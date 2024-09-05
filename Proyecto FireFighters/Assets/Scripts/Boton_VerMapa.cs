using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Boton_VerMapa : MonoBehaviour
{

    public GameObject Texto_FinJuego;
    public bool activo = true;
 

    // Update is called once per frame
    public void Activar_Desactivar()
    {
        if (activo)
        {
            activo = false;
            Texto_FinJuego.SetActive(false);
        }
        else
        {
            activo = true;
            Texto_FinJuego.SetActive(true);
        }
    }
}
