package com.example.clienterep

data class ClientProfile(
    val name: String,
    val points: Int
)

data class RetornoREP(
    val qr_id: String,
    val marca_envase: String,
    val fecha_retorno: Long,
    val estado_retorno: String,
    val peso_envase_kg: Double,
    val destino: String,
    val puntos_otorgados: Int,
    val tienda_retorno: String
)

data class ResumenCliente(
    val profile: ClientProfile,
    val retornos_recientes: List<RetornoREP>,
    val total_retornos: Int,
    val peso_total_kg: Double
)