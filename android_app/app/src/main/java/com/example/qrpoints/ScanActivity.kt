package com.example.qrpoints

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.util.Log
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import com.google.android.material.snackbar.Snackbar
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.common.InputImage
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class ScanActivity : AppCompatActivity() {
    private val TAG = "ScanActivity"
    private lateinit var pointsManager: PointsManager
    private lateinit var cameraExecutor: ExecutorService
    private var profile: String = "default"

    private var toneGen: ToneGenerator? = null
    private var vibrator: Vibrator? = null

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) startCamera() else Log.w(TAG, "Camera permission denied")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scan)

        pointsManager = PointsManager(this)
        cameraExecutor = Executors.newSingleThreadExecutor()

        // setup feedback
        vibrator = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
        toneGen = ToneGenerator(AudioManager.STREAM_MUSIC, 100)

    profile = intent.getStringExtra("profile") ?: "default"
    Log.d(TAG, "ScanActivity started with profile='$profile'")

    val pointsView: TextView = findViewById(R.id.pointsText)
    pointsView.text = "Points: ${pointsManager.getPoints(profile)}"

        // Back button (replaces reset/history)
        val btnBack = findViewById<View>(R.id.btnBack)
        btnBack.setOnClickListener { finish() }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            startCamera()
        } else {
            requestPermissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val previewView = findViewById<androidx.camera.view.PreviewView>(R.id.previewView)
            val preview = Preview.Builder().build().also { p ->
                p.setSurfaceProvider(previewView.surfaceProvider)
            }

            val imageAnalyzer = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()

            imageAnalyzer.setAnalyzer(cameraExecutor) { image ->
                processImageProxy(image)
            }

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this, CameraSelector.DEFAULT_BACK_CAMERA, preview, imageAnalyzer
                )
            } catch (exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun processImageProxy(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image
        if (mediaImage == null) {
            imageProxy.close()
            return
        }

        val image = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)
        val scanner = BarcodeScanning.getClient()

        scanner.process(image)
            .addOnSuccessListener { barcodes ->
                for (barcode in barcodes) {
                    val code = barcode.rawValue ?: continue

                    runOnUiThread {
                        val reward = 100
                        // Defensive: re-read intent extra in case profile changed or was shadowed
                        val intentProfile = intent.getStringExtra("profile") ?: profile
                        Log.d(TAG, "Using profile for redeem: '$intentProfile' (class profile='$profile')")
                        val result = pointsManager.redeemDetailed(code, reward, intentProfile)

                        if (result == "ok") {
                            val pts = pointsManager.getPoints(profile)
                            val pointsTextView = findViewById<TextView>(R.id.pointsText)
                            pointsTextView.text = "$pts / 100 puntos"

                            val progress = findViewById<ProgressBar>(R.id.pointsProgress)
                            progress?.let {
                                it.max = 100
                                it.progress = pts.coerceAtMost(100)
                            }

                            try {
                                vibrator?.let { v ->
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                        v.vibrate(VibrationEffect.createOneShot(160, VibrationEffect.DEFAULT_AMPLITUDE))
                                    } else {
                                        @Suppress("DEPRECATION")
                                        v.vibrate(160)
                                    }
                                }
                                toneGen?.startTone(ToneGenerator.TONE_PROP_ACK, 160)
                            } catch (e: Exception) {
                                Log.w(TAG, "Feedback failed", e)
                            }

                            val title = findViewById<TextView>(R.id.pointsTitle)
                            title.visibility = View.VISIBLE
                            title.postDelayed({ title.visibility = View.GONE }, 1800)

                            val rewardTextView = findViewById<TextView>(R.id.rewardText)
                            rewardTextView.text = "+$reward"

                            val badge = findViewById<View>(R.id.rewardBadge)
                            badge?.let { b ->
                                b.alpha = 0f
                                b.scaleX = 0.6f
                                b.scaleY = 0.6f
                                b.visibility = View.VISIBLE
                                b.animate().alpha(1f).scaleX(1.05f).scaleY(1.05f).setDuration(220).withEndAction {
                                    b.animate().scaleX(0.95f).scaleY(0.95f).setDuration(160).withEndAction {
                                        b.animate().alpha(0f).scaleX(0.6f).scaleY(0.6f).setStartDelay(900).setDuration(320).withEndAction {
                                            b.visibility = View.GONE
                                        }
                                    }
                                }
                            }

                            val previewView = findViewById<View>(R.id.previewView)
                            Snackbar.make(previewView, "+$reward puntos", Snackbar.LENGTH_SHORT).show()

                            // Navigate to PointsActivity showing the selected profile
                            val i = android.content.Intent(this@ScanActivity, PointsActivity::class.java)
                            i.putExtra("profile", intentProfile)
                            startActivity(i)
                            finish()
                        } else {
                            val previewView = findViewById<View>(R.id.previewView)
                            Snackbar.make(previewView, "No se otorgaron puntos: $result (valor: '$code')", Snackbar.LENGTH_LONG).show()
                            Log.d(TAG, "Redeem failed: $result for code '$code'")
                        }
                    }
                }
            }
            .addOnFailureListener { e -> Log.e(TAG, "Barcode failed", e) }
            .addOnCompleteListener { imageProxy.close() }
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
        toneGen?.release()
        toneGen = null
        vibrator = null
    }
}
