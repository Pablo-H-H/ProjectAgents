using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destruir_Tiempo : MonoBehaviour
{
    //Se autodestruye despues del tiempo asignado

    public float tiempo;
    // Start is called before the first frame update
    void Start()
    {
        Invoke("Autodestruir", tiempo);
    }

    public void Autodestruir()
    {
        Destroy(gameObject);
    }
}
