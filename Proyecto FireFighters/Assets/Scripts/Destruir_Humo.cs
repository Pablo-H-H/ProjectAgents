using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destruir_Humo : MonoBehaviour
{
    //Detecta y destruye si tiene el Tag Humo
    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Humo")
        {
            Destroy(other.gameObject);
        }

    }
}
