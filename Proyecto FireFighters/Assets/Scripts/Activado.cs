using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Activado : MonoBehaviour
{
    public int estado_Activado = 0;

    public void cambiarEstado()
    {
        if (estado_Activado == 0)
        {
            estado_Activado = 1;
        }
        else
        {
            estado_Activado = 0;
        }
    }
}
