package com.example.qrpoints

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.appcompat.app.AppCompatActivity

class HistoryActivity : AppCompatActivity() {
    private lateinit var pointsManager: PointsManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)

        pointsManager = PointsManager(this)
        val listView: ListView = findViewById(R.id.historyList)
        val items = pointsManager.getHistory().map { "${it.code} (+${it.points}) — ${java.util.Date(it.date)}" }
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, items)
        listView.adapter = adapter
    }
}
