package com.simple.qrscanner

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.simple.qrscanner.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private val networkService = NetworkService()
    private val CAMERA_PERMISSION_CODE = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupUI()
    }

    private fun setupUI() {
        binding.buttonScan.setOnClickListener {
            val name = binding.editTextName.text.toString().trim()
            
            if (name.isEmpty()) {
                Toast.makeText(this, "Please enter your name first", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            if (checkCameraPermission()) {
                startScanning(name)
            } else {
                requestCameraPermission()
            }
        }
        
        // Add connection test button inspired by spy repository's network testing
        binding.buttonTestConnection.setOnClickListener {
            testServerConnection()
        }
    }
    
    private fun testServerConnection() {
        binding.textViewStatus.text = "Testing server connection..."
        
        networkService.testConnection(object : NetworkService.NetworkCallback {
            override fun onSuccess(response: String) {
                runOnUiThread {
                    binding.textViewStatus.text = "✅ Server connection successful"
                    Toast.makeText(this@MainActivity, "Server is reachable", Toast.LENGTH_SHORT).show()
                }
            }
            
            override fun onError(error: String, errorCode: Int) {
                runOnUiThread {
                    binding.textViewStatus.text = "❌ Connection failed: $error"
                    Toast.makeText(this@MainActivity, "Server connection failed", Toast.LENGTH_LONG).show()
                }
            }
        })
    }

    private fun checkCameraPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun requestCameraPermission() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(Manifest.permission.CAMERA),
            CAMERA_PERMISSION_CODE
        )
    }

    private fun startScanning(userName: String) {
        val intent = Intent(this, ScanActivity::class.java)
        intent.putExtra("USER_NAME", userName)
        startActivityForResult(intent, 1001)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                val name = binding.editTextName.text.toString().trim()
                if (name.isNotEmpty()) {
                    startScanning(name)
                }
            } else {
                Toast.makeText(this, "Camera permission required for QR scanning", Toast.LENGTH_LONG).show()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == 1001) {
            when (resultCode) {
                RESULT_OK -> {
                    val qrCode = data?.getStringExtra("QR_CODE") ?: ""
                    val success = data?.getBooleanExtra("SUCCESS", false) ?: false
                    val response = data?.getStringExtra("RESPONSE") ?: ""
                    val error = data?.getStringExtra("ERROR") ?: ""
                    val errorCode = data?.getIntExtra("ERROR_CODE", -1) ?: -1
                    
                    if (success) {
                        binding.textViewStatus.text = "✅ QR Code sent successfully!\nCode: $qrCode"
                        if (response.isNotEmpty()) {
                            binding.textViewStatus.append("\nServer response: $response")
                        }
                        binding.editTextName.text.clear()
                        Toast.makeText(this, "QR data uploaded to REP server", Toast.LENGTH_SHORT).show()
                    } else {
                        val errorMessage = if (errorCode != -1) {
                            "❌ Failed to send QR code\nError ($errorCode): $error"
                        } else {
                            "❌ Failed to send QR code\nError: $error"
                        }
                        binding.textViewStatus.text = errorMessage
                        Toast.makeText(this, "Upload failed: $error", Toast.LENGTH_LONG).show()
                    }
                }
                RESULT_CANCELED -> {
                    binding.textViewStatus.text = "Scan cancelled"
                }
            }
        }
    }
}