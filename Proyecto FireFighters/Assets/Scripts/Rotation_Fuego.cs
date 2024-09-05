using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using Debug = UnityEngine.Debug;
//using System.Debug;

public class Rotation_Fuego : MonoBehaviour
{
	// Objetivo de rotacion
	public GameObject target;

	// Velocidad Angular
	public float speed = 1.0f;

	private Transform objetivo;


	void Update()
	{
		objetivo = target.GetComponent<Transform>();

		// El step es igual a la velocidad de cada frame.
		float singleStep = speed * Time.deltaTime;

		// Se rota a la velocidad de cada step en el eje foward
		Vector3 newDirection = Vector3.RotateTowards(transform.forward, objetivo.forward, singleStep, 0.0f);

		// Calcula una rotacion a un paso mas cercano a el objetivo y aplica la rotacion
		transform.rotation = Quaternion.LookRotation(newDirection);
	}

}
