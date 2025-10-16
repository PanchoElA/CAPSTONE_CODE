package com.example.clienterep

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class RetornosAdapter(private var retornos: List<RetornoREP>) : 
    RecyclerView.Adapter<RetornosAdapter.RetornoViewHolder>() {

    private val apiClient = ApiClient("http://192.168.5.53:5000") // TODO: hacer configurable

    class RetornoViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val iconDestino: TextView = view.findViewById(R.id.iconDestino)
        val textMarca: TextView = view.findViewById(R.id.textMarca)
        val textDestino: TextView = view.findViewById(R.id.textDestino)
        val textFecha: TextView = view.findViewById(R.id.textFecha)
        val textPuntos: TextView = view.findViewById(R.id.textPuntos)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RetornoViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_retorno, parent, false)
        return RetornoViewHolder(view)
    }

    override fun onBindViewHolder(holder: RetornoViewHolder, position: Int) {
        val retorno = retornos[position]

        holder.textMarca.text = retorno.marca_envase
        holder.textFecha.text = apiClient.formatDate(retorno.fecha_retorno)
        holder.textPuntos.text = "+${retorno.puntos_otorgados}"

        // Configurar según destino
        when (retorno.destino) {
            "REUSO_CODELPA" -> {
                holder.iconDestino.text = "♻️"
                holder.textDestino.text = "Reuso CODELPA"
                holder.textDestino.setTextColor(
                    holder.itemView.context.getColor(R.color.success)
                )
            }
            "VALORIZACION_INPROPLAS" -> {
                holder.iconDestino.text = "🏭"
                holder.textDestino.text = "Valorización Inproplas"
                holder.textDestino.setTextColor(
                    holder.itemView.context.getColor(R.color.warning)
                )
            }
            else -> {
                holder.iconDestino.text = "📦"
                holder.textDestino.text = retorno.destino
                holder.textDestino.setTextColor(
                    holder.itemView.context.getColor(android.R.color.darker_gray)
                )
            }
        }
    }

    override fun getItemCount() = retornos.size

    fun updateRetornos(newRetornos: List<RetornoREP>) {
        retornos = newRetornos
        notifyDataSetChanged()
    }
}