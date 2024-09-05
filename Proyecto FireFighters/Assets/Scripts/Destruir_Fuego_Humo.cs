using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destruir_Fuego_Humo : MonoBehaviour
{
	//Detecta y destruye si tiene el Tag Humo o Fuego
	void OnTriggerEnter(Collider other)
	{
		if (other.gameObject.tag == "Humo" || other.gameObject.tag == "Fuego")
		{
			Destroy(other.gameObject);
		}
	}
}
