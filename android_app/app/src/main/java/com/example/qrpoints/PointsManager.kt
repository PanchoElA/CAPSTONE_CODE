package com.example.qrpoints

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.net.URLDecoder
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.concurrent.Executors
import java.util.*

data class ScanRecord(val id: String, val code: String, val points: Int, val date: Long)

class PointsManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("qrpoints", Context.MODE_PRIVATE)
    private val gson = Gson()

    // Solo acepta QRs REP del sistema desktop (CODELPA: y TERCERO:)
    // Server base URL for remote sync - con fallbacks para problemas de red
    private val DEFAULT_SERVER_BASE = "http://192.168.5.53:5000"
    private val FALLBACK_SERVER_BASE = "http://localhost:5000"
    private val SERVER_BASE: String
    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
        .writeTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
        .build()
    private val httpExecutor = Executors.newSingleThreadExecutor()

    init {
        // Read server base from prefs, fallback to default
        SERVER_BASE = prefs.getString("server_base", DEFAULT_SERVER_BASE) ?: DEFAULT_SERVER_BASE
        Log.d("PointsManager", "Initialized with server: $SERVER_BASE")
    }

    // Función para probar conectividad y encontrar servidor que funcione
    private fun getWorkingServerUrl(): String {
        val serversToTry = listOf(
            SERVER_BASE,
            DEFAULT_SERVER_BASE,
            FALLBACK_SERVER_BASE
        ).distinct()

        for (serverUrl in serversToTry) {
            try {
                Log.d("PointsManager", "Testing connectivity to: $serverUrl")
                val testRequest = Request.Builder()
                    .url("$serverUrl/")
                    .get()
                    .build()
                
                httpClient.newCall(testRequest).execute().use { response ->
                    if (response.isSuccessful) {
                        Log.d("PointsManager", "Successfully connected to: $serverUrl")
                        return serverUrl
                    }
                }
            } catch (e: Exception) {
                Log.w("PointsManager", "Failed to connect to $serverUrl: ${e.message}")
            }
        }
        
        Log.e("PointsManager", "No working server found, using default: $SERVER_BASE")
        return SERVER_BASE
    }

    // Extract a canonical id from many possible QR payload shapes.
    // SOLO acepta QRs REP generados por la aplicación desktop
    private fun extractIdFromCode(raw: String): String? {
        if (raw.isBlank()) return null
        // Trim
        var s = raw.trim()

        // Try URL-decoding once (safe fallback)
        try {
            val decoded = URLDecoder.decode(s, "UTF-8")
            if (decoded.isNotEmpty()) s = decoded
        } catch (e: Exception) {
            // ignore decoding errors
        }

        // SOLO QRs REP del sistema desktop (CODELPA: o TERCERO:)
        if (s.startsWith("CODELPA:", ignoreCase = true) || s.startsWith("TERCERO:", ignoreCase = true)) {
            // Validar formato específico: TIPO:XXXXXXXXXXXX (exactamente 12 caracteres hex después del :)
            val parts = s.split(":")
            if (parts.size == 2) {
                val tipo = parts[0].uppercase()
                val codigo = parts[1].uppercase()
                
                // Validar que el código tenga exactamente 12 caracteres hexadecimales
                if (codigo.length == 12 && codigo.matches(Regex("^[A-F0-9]{12}$"))) {
                    val qrCompleto = "$tipo:$codigo"
                    Log.d("PointsManager", "extractIdFromCode: QR REP válido detectado='$qrCompleto'")
                    return qrCompleto
                } else {
                    Log.w("PointsManager", "extractIdFromCode: QR REP inválido - código debe ser 12 caracteres hex: '$codigo'")
                    return null
                }
            } else {
                Log.w("PointsManager", "extractIdFromCode: QR REP inválido - formato incorrecto: '$s'")
                return null
            }
        }

        // RECHAZAR todos los demás formatos (sin prefijo REP, URLs, texto plano, etc.)
        Log.w("PointsManager", "extractIdFromCode: QR rechazado - solo se aceptan QRs REP del sistema: '$raw'")
        return null
    }

    // get points for a named profile (default profile = "default")
    fun getPoints(profile: String = "default"): Int {
        return prefs.getInt("points_$profile", 0)
    }

    fun redeem(code: String, points: Int, profile: String = "default"): Boolean {
        // Usar redeemDetailed para validación completa
        val result = redeemDetailed(code, points, profile)
        return result.startsWith("ok_rep_") // Solo éxito si es QR REP procesado
    }

    // Debug-friendly version that returns a brief status message
    // SOLO acepta QRs REP del sistema desktop
    fun redeemDetailed(code: String, points: Int, profile: String = "default"): String {
        val id = extractIdFromCode(code) ?: return "qr_no_valido_sistema_rep"
        if (id.isEmpty()) return "qr_vacio"
        
        Log.d("PointsManager", "redeemDetailed: processing code='$code' id='$id' profile='$profile'")
        
        // Validación adicional: DEBE ser QR REP del sistema
        if (!id.startsWith("CODELPA:") && !id.startsWith("TERCERO:")) {
            Log.w("PointsManager", "redeemDetailed: QR rechazado - no es del sistema REP: '$id'")
            return "qr_solo_sistema_rep"
        }
        
        // Procesar QR REP válido
        Log.d("PointsManager", "redeemDetailed: QR REP válido, procesando via endpoint REP")
        return redeemREP(id, profile)
    }

    private fun redeemREP(qrId: String, profile: String): String {
        Log.d("PointsManager", "Processing REP QR: $qrId for profile: $profile")
        
        // Verificar si ya fue usado
        val redeemed = getHistoryIds(profile).toMutableSet()
        if (redeemed.contains(qrId)) {
            Log.w("PointsManager", "REP QR already redeemed: $qrId")
            return "already_redeemed"
        }

        // Obtener servidor que funcione
        val workingServerUrl = getWorkingServerUrl()
        Log.d("PointsManager", "Using server: $workingServerUrl")
        
        // Simular validación de estado (en la app real sería un checklist)
        val estadoRetorno = "BUENO" // TODO: capturar desde UI
        val tiendaRetorno = "MUNDO_PINTURA_CENTRAL" // TODO: desde configuración
        val evidencia = "INSPECCION_VISUAL" // TODO: foto/checklist
        
        try {
            val payload = mapOf(
                "qr_id" to qrId,
                "estado_retorno" to estadoRetorno,
                "tienda_retorno" to tiendaRetorno,
                "cliente_profile" to profile,
                "evidencia" to evidencia
            )
            val json = gson.toJson(payload)
            val mediaType = "application/json; charset=utf-8".toMediaType()
            val body = json.toRequestBody(mediaType)
            val req = Request.Builder()
                .url("$workingServerUrl/retorno_rep")
                .post(body)
                .addHeader("Content-Type", "application/json")
                .build()
            
            Log.d("PointsManager", "Sending REP request to: $workingServerUrl/retorno_rep")
            Log.d("PointsManager", "REP payload: $json")
            
            // Hacer llamada síncrona para verificar resultado inmediatamente
            try {
                httpClient.newCall(req).execute().use { resp ->
                    val responseBody = resp.body?.string()
                    Log.d("PointsManager", "REP response: ${resp.code} - $responseBody")
                    
                    if (resp.isSuccessful && responseBody != null) {
                        try {
                            val result = gson.fromJson(responseBody, Map::class.java)
                            val puntosOtorgados = (result["puntos_otorgados"] as? Double)?.toInt() ?: 0
                            val destino = result["destino"] as? String ?: "UNKNOWN"
                            
                            if (puntosOtorgados > 0) {
                                // Actualizar puntos localmente
                                val currentPoints = getPoints(profile)
                                val newPoints = currentPoints + puntosOtorgados
                                prefs.edit().putInt("points_$profile", newPoints).apply()
                                
                                // Guardar registro local
                                saveHistoryRecord(ScanRecord(qrId, qrId, puntosOtorgados, Date().time), profile)
                                
                                Log.d("PointsManager", "REP success: $puntosOtorgados points added, destino: $destino, new total: $newPoints")
                                return "ok_rep_${puntosOtorgados}_points"
                            } else {
                                Log.w("PointsManager", "REP processed but no points awarded")
                                return "rep_no_points"
                            }
                        } catch (e: Exception) {
                            Log.e("PointsManager", "Error parsing REP response: $responseBody", e)
                            return "rep_parse_error"
                        }
                    } else {
                        Log.e("PointsManager", "REP request failed: ${resp.code} - $responseBody")
                        return "rep_server_error_${resp.code}"
                    }
                }
            } catch (e: java.net.ConnectException) {
                Log.e("PointsManager", "REP connection refused - server may be down", e)
                return "rep_connection_refused"
            } catch (e: java.net.SocketTimeoutException) {
                Log.e("PointsManager", "REP request timeout - slow network", e)
                return "rep_timeout"
            } catch (e: java.net.UnknownHostException) {
                Log.e("PointsManager", "REP unknown host - check server URL", e)
                return "rep_unknown_host"
            } catch (e: java.io.IOException) {
                Log.e("PointsManager", "REP IO error - network issue", e)
                return "rep_network_error"
            } catch (e: Exception) {
                Log.e("PointsManager", "REP unexpected network error", e)
                return "rep_network_error"
            }
            
        } catch (e: Exception) {
            Log.e("PointsManager", "REP redeem failed", e)
            return "rep_error"
        }
    }

    private fun saveHistoryRecord(record: ScanRecord, profile: String = "default") {
        val history = getHistory(profile).toMutableList()
        history.add(0, record)
        val json = gson.toJson(history)
        prefs.edit().putString("history_$profile", json).apply()
    }

    fun getHistory(profile: String = "default"): List<ScanRecord> {
        val json = prefs.getString("history_$profile", null) ?: return emptyList()
        val type = object : TypeToken<List<ScanRecord>>() {}.type
        return gson.fromJson(json, type)
    }

    private fun getHistoryIds(profile: String = "default"): Set<String> {
        return getHistory(profile).map { it.id }.toSet()
    }

    // Reset all data for debugging (clears all profiles)
    fun reset() {
        prefs.edit().clear().apply()
    }

    // Return list of profiles detected from stored keys
    fun getProfiles(): List<String> {
        val set = mutableSetOf<String>()
        for (entry in prefs.all.keys) {
            if (entry.startsWith("points_")) {
                set.add(entry.removePrefix("points_"))
            } else if (entry.startsWith("history_")) {
                set.add(entry.removePrefix("history_"))
            }
        }
        return set.toList()
    }
}
