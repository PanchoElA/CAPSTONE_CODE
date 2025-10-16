package com.example.clienterep

import android.os.Bundle
import android.view.MenuItem
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import kotlinx.coroutines.*

class HistorialActivity : AppCompatActivity() {
    
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var progressBar: ProgressBar
    private lateinit var recyclerHistorial: RecyclerView
    private lateinit var emptyState: TextView
    
    private lateinit var retornosAdapter: RetornosAdapter
    private lateinit var apiClient: ApiClient
    
    private var clienteNombre: String? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_historial)
        
        setupActionBar()
        initViews()
        setupApiClient()
        setupRecyclerView()
        setupListeners()
        
        clienteNombre = intent.getStringExtra("cliente_nombre")
        if (clienteNombre != null) {
            title = "Historial de $clienteNombre"
            cargarHistorial()
        } else {
            finish()
        }
    }
    
    private fun setupActionBar() {
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
    }
    
    private fun initViews() {
        swipeRefresh = findViewById(R.id.swipeRefresh)
        progressBar = findViewById(R.id.progressBar)
        recyclerHistorial = findViewById(R.id.recyclerHistorial)
        emptyState = findViewById(R.id.emptyState)
        
        val prefs = getSharedPreferences("cliente_rep", MODE_PRIVATE)
        val serverBase = prefs.getString("server_base", "http://192.168.5.53:5000") ?: "http://192.168.5.53:5000"
        apiClient = ApiClient(serverBase)
    }
    
    private fun setupApiClient() {
        val prefs = getSharedPreferences("cliente_rep", MODE_PRIVATE)
        val serverBase = prefs.getString("server_base", "http://192.168.5.53:5000") ?: "http://192.168.5.53:5000"
        apiClient = ApiClient(serverBase)
    }
    
    private fun setupRecyclerView() {
        retornosAdapter = RetornosAdapter(emptyList())
        recyclerHistorial.layoutManager = LinearLayoutManager(this)
        recyclerHistorial.adapter = retornosAdapter
    }
    
    private fun setupListeners() {
        swipeRefresh.setOnRefreshListener {
            cargarHistorial()
        }
    }
    
    private fun cargarHistorial() {
        showLoading(true)
        
        CoroutineScope(Dispatchers.Main).launch {
            try {
                val retornos = withContext(Dispatchers.IO) {
                    apiClient.getRetornosCliente(clienteNombre!!)
                }
                
                if (retornos.isNotEmpty()) {
                    retornosAdapter.updateRetornos(retornos)
                    recyclerHistorial.visibility = View.VISIBLE
                    emptyState.visibility = View.GONE
                } else {
                    recyclerHistorial.visibility = View.GONE
                    emptyState.visibility = View.VISIBLE
                }
            } catch (e: Exception) {
                Toast.makeText(this@HistorialActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            } finally {
                showLoading(false)
            }
        }
    }
    
    private fun showLoading(show: Boolean) {
        swipeRefresh.isRefreshing = false
        progressBar.visibility = if (show) View.VISIBLE else View.GONE
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            android.R.id.home -> {
                onBackPressed()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}