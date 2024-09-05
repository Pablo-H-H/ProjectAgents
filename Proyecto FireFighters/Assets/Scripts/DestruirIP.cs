using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DestruirIP : MonoBehaviour
{
	//Detecta y destruye si tiene el Tag InterestPoint
	void OnTriggerEnter(Collider other)
	{
		if (other.gameObject.tag == "InterestPoint")
		{
			Destroy(other.gameObject);
		}
	}
}
