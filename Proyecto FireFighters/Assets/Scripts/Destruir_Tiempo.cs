using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destruir_Tiempo : MonoBehaviour
{

    public float tiempo;
    // Start is called before the first frame update
    void Start()
    {
        Invoke("Autodestruir", tiempo);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Autodestruir()
    {
        Destroy(gameObject);
    }
}
