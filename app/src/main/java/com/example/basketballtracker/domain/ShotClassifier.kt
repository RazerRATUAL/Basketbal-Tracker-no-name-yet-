package com.example.basketballtracker.domain

import android.graphics.RectF
import kotlin.math.abs

enum class ShotState {
    TRACKING,
    MAKE,
    MISS
}

class ShotClassifier(private val rimBounds: RectF) {
    private val rimCenterX = rimBounds.centerX()
    private val rimRadius = rimBounds.width() / 2f

    private var aboveRimEntry = false
    private var passedCylinder = false
    var currentState = ShotState.TRACKING
        private set

    fun update(ballX: Float, ballY: Float): ShotState {
        // 1. Ball enters space horizontally aligned above the rim
        if (ballX in rimBounds.left..rimBounds.right && ballY < rimBounds.top) {
            aboveRimEntry = true
        }

        // 2. Ball descends through the horizontal cylinder
        if (aboveRimEntry && ballY in rimBounds.top..rimBounds.bottom) {
            if (abs(ballX - rimCenterX) < (rimRadius * 0.9f)) {
                passedCylinder = true
            }
        }

        // 3. Clean exit through the net bottom
        if (passedCylinder && ballY > rimBounds.bottom + 20f) {
            currentState = ShotState.MAKE
            return currentState
        }

        // 4. Dropped past rim without clearing cylinder cleanly
        if (ballY > rimBounds.bottom + 50f && !passedCylinder) {
            currentState = ShotState.MISS
            return currentState
        }

        return currentState
    }

    fun reset() {
        aboveRimEntry = false
        passedCylinder = false
        currentState = ShotState.TRACKING
    }
}