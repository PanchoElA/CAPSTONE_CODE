package com.example.clienterep

import android.util.Log
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import okhttp3.OkHttpClient
import okhttp3.Request
import java.text.SimpleDateFormat
import java.util.*
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine

class ApiClient(private val serverBase: String) {
    private val client = OkHttpClient()
    private val gson = Gson()

    suspend fun getClientProfile(clientName: String): ClientProfile? = suspendCoroutine { continuation ->
        try {
            val request = Request.Builder()
                .url("$serverBase/profiles")
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val json = response.body?.string()
                    if (json != null) {
                        val type = object : TypeToken<List<ClientProfile>>() {}.type
                        val profiles: List<ClientProfile> = gson.fromJson(json, type)
                        val profile = profiles.find { it.name.equals(clientName, ignoreCase = true) }
                        continuation.resume(profile)
                    } else {
                        continuation.resume(null)
                    }
                } else {
                    Log.e("ApiClient", "Error getting profiles: ${response.code}")
                    continuation.resume(null)
                }
            }
        } catch (e: Exception) {
            Log.e("ApiClient", "Exception getting profile", e)
            continuation.resume(null)
        }
    }

    suspend fun getClientRetornos(clientName: String): List<RetornoREP> = suspendCoroutine { continuation ->
        try {
            // Obtener retornos del cliente desde la BD REP
            val request = Request.Builder()
                .url("$serverBase/cliente_retornos/$clientName")
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val json = response.body?.string()
                    if (json != null) {
                        val type = object : TypeToken<List<RetornoREP>>() {}.type
                        val retornos: List<RetornoREP> = gson.fromJson(json, type)
                        continuation.resume(retornos)
                    } else {
                        continuation.resume(emptyList())
                    }
                } else {
                    Log.e("ApiClient", "Error getting retornos: ${response.code}")
                    continuation.resume(emptyList())
                }
            }
        } catch (e: Exception) {
            Log.e("ApiClient", "Exception getting retornos", e)
            continuation.resume(emptyList())
        }
    }

    suspend fun getResumenCliente(clientName: String): ResumenCliente? = suspendCoroutine { continuation ->
        try {
            // Obtener datos del cliente desde el endpoint combinado
            val request = Request.Builder()
                .url("$serverBase/cliente_retornos/$clientName")
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val json = response.body?.string()
                    if (json != null) {
                        val resumen: ResumenCliente = gson.fromJson(json, ResumenCliente::class.java)
                        continuation.resume(resumen)
                    } else {
                        continuation.resume(null)
                    }
                } else {
                    Log.e("ApiClient", "Error getting resumen: ${response.code}")
                    continuation.resume(null)
                }
            }
        } catch (e: Exception) {
            Log.e("ApiClient", "Exception getting resumen", e)
            continuation.resume(null)
        }
    }

    suspend fun getRetornosCliente(clientName: String): List<RetornoREP> = suspendCoroutine { continuation ->
        try {
            val request = Request.Builder()
                .url("$serverBase/retornos_completos/$clientName")
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val json = response.body?.string()
                    if (json != null) {
                        val type = object : TypeToken<List<RetornoREP>>() {}.type
                        val retornos: List<RetornoREP> = gson.fromJson(json, type)
                        continuation.resume(retornos)
                    } else {
                        continuation.resume(emptyList())
                    }
                } else {
                    Log.e("ApiClient", "Error getting retornos completos: ${response.code}")
                    continuation.resume(emptyList())
                }
            }
        } catch (e: Exception) {
            Log.e("ApiClient", "Exception getting retornos completos", e)
            continuation.resume(emptyList())
        }
    }

    fun formatDate(timestamp: Long): String {
        return try {
            val date = Date(timestamp)
            val format = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
            format.format(date)
        } catch (e: Exception) {
            "Fecha inválida"
        }
    }
}