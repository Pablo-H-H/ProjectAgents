using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DestructorPared : MonoBehaviour
{
    //Detecta y destruye si tiene el Tag Pared
    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Pared")
        {
            Destroy(other.gameObject);
        }

    }
}