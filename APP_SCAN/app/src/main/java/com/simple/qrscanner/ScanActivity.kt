package com.simple.qrscanner

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import com.simple.qrscanner.databinding.ActivityScanBinding
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class ScanActivity : AppCompatActivity() {
    private lateinit var binding: ActivityScanBinding
    private lateinit var cameraExecutor: ExecutorService
    private var userName: String = ""
    private var isProcessing = false
    
    private val networkService = NetworkService()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityScanBinding.inflate(layoutInflater)
        setContentView(binding.root)

        userName = intent.getStringExtra("USER_NAME") ?: ""
        
        setupUI()
        startCamera()
        
        cameraExecutor = Executors.newSingleThreadExecutor()
    }

    private fun setupUI() {
        binding.buttonBack.setOnClickListener {
            setResult(RESULT_CANCELED)
            finish()
        }
        
        binding.textViewResult.text = "Point camera at QR code\nUser: $userName"
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(binding.previewView.surfaceProvider)
            }

            val imageAnalyzer = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
                .also {
                    it.setAnalyzer(cameraExecutor, QRCodeAnalyzer { qrCode ->
                        if (!isProcessing) {
                            isProcessing = true
                            runOnUiThread {
                                binding.textViewResult.text = "QR Code found: $qrCode\nSending to server..."
                            }
                            sendQRToServer(qrCode)
                        }
                    })
                }

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageAnalyzer
                )
            } catch (exc: Exception) {
                Log.e("ScanActivity", "Use case binding failed", exc)
                runOnUiThread {
                    Toast.makeText(this, "Camera initialization failed", Toast.LENGTH_SHORT).show()
                }
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private fun sendQRToServer(qrCode: String) {
        runOnUiThread {
            binding.textViewResult.text = "QR Code found: $qrCode\nSending to server..."
        }
        
        networkService.sendQRData(qrCode, userName, object : NetworkService.NetworkCallback {
            override fun onSuccess(response: String) {
                runOnUiThread {
                    Log.d("ScanActivity", "Server response: $response")
                    binding.textViewResult.text = "✅ Success! QR sent to server"
                    
                    val resultIntent = Intent().apply {
                        putExtra("QR_CODE", qrCode)
                        putExtra("SUCCESS", true)
                        putExtra("RESPONSE", response)
                    }
                    setResult(RESULT_OK, resultIntent)
                    
                    binding.textViewResult.postDelayed({
                        finish()
                    }, 2000)
                }
            }
            
            override fun onError(error: String, errorCode: Int) {
                runOnUiThread {
                    val errorMessage = if (errorCode != -1) {
                        "❌ Error ($errorCode): $error"
                    } else {
                        "❌ $error"
                    }
                    
                    binding.textViewResult.text = errorMessage
                    Log.e("ScanActivity", "Network error: $error (Code: $errorCode)")
                    
                    val resultIntent = Intent().apply {
                        putExtra("QR_CODE", qrCode)
                        putExtra("SUCCESS", false)
                        putExtra("ERROR", error)
                        putExtra("ERROR_CODE", errorCode)
                    }
                    setResult(RESULT_OK, resultIntent)
                    
                    binding.textViewResult.postDelayed({
                        isProcessing = false // Allow retry
                    }, 3000)
                }
            }
        })
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }

    private class QRCodeAnalyzer(private val listener: (String) -> Unit) : ImageAnalysis.Analyzer {
        private val scanner = BarcodeScanning.getClient()

        override fun analyze(imageProxy: ImageProxy) {
            val mediaImage = imageProxy.image
            if (mediaImage != null) {
                val image = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)
                scanner.process(image)
                    .addOnSuccessListener { barcodes ->
                        for (barcode in barcodes) {
                            when (barcode.valueType) {
                                Barcode.TYPE_TEXT, Barcode.TYPE_URL -> {
                                    barcode.rawValue?.let { value ->
                                        listener(value)
                                    }
                                }
                            }
                        }
                    }
                    .addOnFailureListener {
                        Log.e("QRCodeAnalyzer", "Barcode scanning failed", it)
                    }
                    .addOnCompleteListener {
                        imageProxy.close()
                    }
            } else {
                imageProxy.close()
            }
        }
    }
}