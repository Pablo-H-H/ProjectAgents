using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerAtaca : MonoBehaviour
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
			GameObject playerRescued = other.gameObject;
			playerRescued.GetComponent<PlayerMovement>().pateando = true;


		}
	}


}
