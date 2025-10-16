package com.example.clienterep

import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import kotlinx.coroutines.*

class MainActivity : AppCompatActivity() {
    
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var inputNombre: EditText
    private lateinit var btnBuscar: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var contentContainer: LinearLayout
    private lateinit var textPuntos: TextView
    private lateinit var textRetornos: TextView
    private lateinit var textPeso: TextView
    private lateinit var recyclerHistorial: RecyclerView
    private lateinit var btnVerTodo: Button
    private lateinit var emptyState: LinearLayout
    private lateinit var welcomeText: TextView
    
    private lateinit var retornosAdapter: RetornosAdapter
    private lateinit var apiClient: ApiClient
    private lateinit var prefs: SharedPreferences
    
    private var currentClientName: String? = null
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupApiClient()
        setupRecyclerView()
        setupListeners()
        loadSavedClient()
    }
    
    private fun initViews() {
        swipeRefresh = findViewById(R.id.swipeRefresh)
        inputNombre = findViewById(R.id.inputNombre)
        btnBuscar = findViewById(R.id.btnBuscar)
        progressBar = findViewById(R.id.progressBar)
        contentContainer = findViewById(R.id.contentContainer)
        textPuntos = findViewById(R.id.textPuntos)
        textRetornos = findViewById(R.id.textRetornos)
        textPeso = findViewById(R.id.textPeso)
        recyclerHistorial = findViewById(R.id.recyclerHistorial)
        btnVerTodo = findViewById(R.id.btnVerTodo)
        emptyState = findViewById(R.id.emptyState)
        welcomeText = findViewById(R.id.welcomeText)
        
        prefs = getSharedPreferences("cliente_rep", MODE_PRIVATE)
    }
    
    private fun setupApiClient() {
        // TODO: hacer configurable desde Settings
        val serverBase = prefs.getString("server_base", "http://192.168.5.53:5000") ?: "http://192.168.5.53:5000"
        apiClient = ApiClient(serverBase)
    }
    
    private fun setupRecyclerView() {
        retornosAdapter = RetornosAdapter(emptyList())
        recyclerHistorial.layoutManager = LinearLayoutManager(this)
        recyclerHistorial.adapter = retornosAdapter
    }
    
    private fun setupListeners() {
        btnBuscar.setOnClickListener {
            val nombre = inputNombre.text.toString().trim()
            if (nombre.isNotEmpty()) {
                buscarCliente(nombre)
            } else {
                Toast.makeText(this, "Ingresa tu nombre", Toast.LENGTH_SHORT).show()
            }
        }
        
        btnVerTodo.setOnClickListener {
            currentClientName?.let { nombre ->
                val intent = Intent(this, HistorialActivity::class.java)
                intent.putExtra("cliente_nombre", nombre)
                startActivity(intent)
            }
        }
        
        swipeRefresh.setOnRefreshListener {
            currentClientName?.let { buscarCliente(it) }
        }
        
        // Enter key en el campo de nombre
        inputNombre.setOnEditorActionListener { _, _, _ ->
            btnBuscar.performClick()
            true
        }
    }
    
    private fun loadSavedClient() {
        val savedName = prefs.getString("last_client_name", null)
        if (!savedName.isNullOrEmpty()) {
            inputNombre.setText(savedName)
            welcomeText.text = "¡Hola otra vez, $savedName!"
        }
    }
    
    private fun buscarCliente(nombre: String) {
        showLoading(true)
        
        CoroutineScope(Dispatchers.Main).launch {
            try {
                val resumen = withContext(Dispatchers.IO) {
                    apiClient.getResumenCliente(nombre)
                }
                
                if (resumen != null) {
                    mostrarResumen(resumen)
                    saveClientName(nombre)
                } else {
                    showError("Cliente '$nombre' no encontrado.\n¿Has devuelto algún balde?")
                }
            } catch (e: Exception) {
                showError("Error de conexión: ${e.message}")
            } finally {
                showLoading(false)
            }
        }
    }
    
    private fun mostrarResumen(resumen: ResumenCliente) {
        currentClientName = resumen.profile.name
        
        welcomeText.text = "¡Hola, ${resumen.profile.name}!"
        textPuntos.text = resumen.profile.points.toString()
        textRetornos.text = resumen.total_retornos.toString()
        textPeso.text = "${String.format("%.1f", resumen.peso_total_kg)} kg"
        
        if (resumen.retornos_recientes.isNotEmpty()) {
            retornosAdapter.updateRetornos(resumen.retornos_recientes)
            recyclerHistorial.visibility = View.VISIBLE
            emptyState.visibility = View.GONE
            btnVerTodo.visibility = if (resumen.total_retornos > resumen.retornos_recientes.size) View.VISIBLE else View.GONE
        } else {
            recyclerHistorial.visibility = View.GONE
            emptyState.visibility = View.VISIBLE
            btnVerTodo.visibility = View.GONE
        }
        
        contentContainer.visibility = View.VISIBLE
    }
    
    private fun saveClientName(nombre: String) {
        prefs.edit().putString("last_client_name", nombre).apply()
    }
    
    private fun showLoading(show: Boolean) {
        swipeRefresh.isRefreshing = false
        progressBar.visibility = if (show) View.VISIBLE else View.GONE
        contentContainer.visibility = if (show) View.GONE else contentContainer.visibility
        btnBuscar.isEnabled = !show
    }
    
    private fun showError(message: String) {
        contentContainer.visibility = View.GONE
        Toast.makeText(this, message, Toast.LENGTH_LONG).show()
    }
}