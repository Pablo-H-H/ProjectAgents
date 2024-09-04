using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerCargando : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
	void OnTriggerEnter(Collider other)
	{
		if (other.gameObject.tag == "Player")
		{
			GameObject playerRescued = other.transform.GetChild(0).gameObject;
			if(playerRescued.GetComponent<Activado>().estado_Activado == 0)
			{
				playerRescued.SetActive(true);
				playerRescued.GetComponent<Activado>().cambiarEstado();
			}
			else
			{
				playerRescued.GetComponent<Activado>().cambiarEstado();
				playerRescued.SetActive(false);
			}
			

		}
	}



}
