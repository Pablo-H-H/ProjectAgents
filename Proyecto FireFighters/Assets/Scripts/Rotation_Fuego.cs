using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using Debug = UnityEngine.Debug;
//using System.Debug;

public class Rotation_Fuego : MonoBehaviour
{
	// The target marker.
	public GameObject target;

	// Angular speed in radians per sec.
	public float speed = 1.0f;

	private Transform objetivo;

	void Start()
	{
		objetivo = target.GetComponent<Transform>();
	}

	void Update()
	{
		objetivo = target.GetComponent<Transform>();

		// The step size is equal to speed times frame time.
		float singleStep = speed * Time.deltaTime;

		// Rotate the forward vector towards the objetivo direction by one step
		Vector3 newDirection = Vector3.RotateTowards(transform.forward, objetivo.forward, singleStep, 0.0f);

		// Calculate a rotation a step closer to the objetivo and applies rotation to this object
		transform.rotation = Quaternion.LookRotation(newDirection);
	}

}
