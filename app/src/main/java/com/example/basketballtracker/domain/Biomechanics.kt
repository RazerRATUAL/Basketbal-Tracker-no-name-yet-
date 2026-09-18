package com.example.basketballtracker.domain

import kotlin.math.acos
import kotlin.math.sqrt

data class Point3D(val x: Float, val y: Float, val z: Float)

data class ShotMechanicsResult(
    val elbowAngle: Float,
    val shoulderElevation: Float,
    val feedback: List<String>
)

object Biomechanics {

    fun calculateAngle3D(a: Point3D, b: Point3D, c: Point3D): Float {
        // Vector BA (b to a)
        val baX = a.x - b.x
        val baY = a.y - b.y
        val baZ = a.z - b.z

        // Vector BC (b to c)
        val bcX = c.x - b.x
        val bcY = c.y - b.y
        val bcZ = c.z - b.z

        // Dot product
        val dotProduct = (baX * bcX) + (baY * bcY) + (baZ * bcZ)

        // Magnitudes
        val magBA = sqrt(baX * baX + baY * baY + baZ * baZ)
        val magBC = sqrt(bcX * bcX + bcY * bcY + bcZ * bcZ)

        if (magBA == 0f || magBC == 0f) return 0f

        val cosine = (dotProduct / (magBA * magBC)).coerceIn(-1.0f, 1.0f)
        return Math.toDegrees(acos(cosine.toDouble())).toFloat()
    }

    fun evaluateShot(shoulder: Point3D, elbow: Point3D, wrist: Point3D, hip: Point3D): ShotMechanicsResult {
        val elbowAngle = calculateAngle3D(shoulder, elbow, wrist)
        val shoulderElevation = calculateAngle3D(hip, shoulder, elbow)

        val feedback = mutableListOf<String>()

        if (elbowAngle < 155f) {
            feedback.add("Short arm release (${"%.1f".format(elbowAngle)}°). Extend fully toward the basket.")
        } else {
            feedback.add("Solid extension through release (${"%.1f".format(elbowAngle)}°).")
        }

        if (shoulderElevation < 110f) {
            feedback.add("Low release point (${"%.1f".format(shoulderElevation)}°). Push shooting pocket higher.")
        } else {
            feedback.add("Good release height promotes higher arc.")
        }

        return ShotMechanicsResult(elbowAngle, shoulderElevation, feedback)
    }
}