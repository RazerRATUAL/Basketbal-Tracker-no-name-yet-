import numpy as np

def calculate_angle_3d(point_a, point_b, point_c):
    """
    Calculates the 3D angle at point_b formed by segment BA and BC.
    point_a, point_b, point_c: (x, y, z) tuples or arrays
    """
    a = np.array(point_a)
    b = np.array(point_b)  # Vertex (e.g., Elbow)
    c = np.array(point_c)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    return float(np.degrees(np.arccos(cosine_angle)))

def evaluate_shot_mechanics(shoulder, elbow, wrist, hip):
    """
    Evaluates arm extension and release mechanics at the apex release frame.
    """
    elbow_angle = calculate_angle_3d(shoulder, elbow, wrist)
    shoulder_elevation = calculate_angle_3d(hip, shoulder, elbow)

    feedback = []
    
    if elbow_angle < 155.0:
        feedback.append(f"Short arm release ({elbow_angle:.1f}°). Aim for full extension (~165°-175°).")
    else:
        feedback.append(f"Solid extension through release ({elbow_angle:.1f}°).")

    if shoulder_elevation < 110.0:
        feedback.append(f"Low release height ({shoulder_elevation:.1f}°). Push the release pocket upward.")
    else:
        feedback.append("Release height promotes a high arc trajectory.")

    return {
        "elbow_angle": elbow_angle,
        "shoulder_elevation": shoulder_elevation,
        "feedback": feedback
    }

if __name__ == "__main__":
    # Test coordinates (Hip, Shoulder, Elbow, Wrist in 3D meters)
    mock_hip = (0.2, 0.9, 0.1)
    mock_shoulder = (0.2, 0.4, 0.1)
    mock_elbow = (0.25, 0.15, 0.2)
    mock_wrist = (0.27, -0.1, 0.25)

    results = evaluate_shot_mechanics(mock_shoulder, mock_elbow, mock_wrist, mock_hip)
    print("--- Biomechanics Check ---")
    for key, value in results.items():
        print(f"{key}: {value}")
