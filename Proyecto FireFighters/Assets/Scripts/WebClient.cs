// TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEditor;
using UnityEngine;
using System.IO;
using UnityEngine.Networking;
using System.Linq;

using Debug = UnityEngine.Debug;
using System.Collections.Specialized;
using System;

public class WebClient : MonoBehaviour
{
	[Header("Paredes, puertas y entradas")]
	public GameObject pared;
	public GameObject paredDaniada;
	public GameObject paredDestruida;
	public GameObject puerta;		
	public GameObject puerta_entrada;

	[Header("Bomberos y entorno")]
	public GameObject humo;
	public GameObject fuego;
	public GameObject bombero;
	public GameObject puntoInteres;

	[Header("Bomberos y entorno")]
	public GameObject Fin_Juego;
	public GameObject VerMapa;

	[Header("Triggers Entorno")]
	public GameObject destruir_humo_fuego;
	public GameObject destruirMuro;
	public GameObject DescubrirIP;
	public GameObject destruirIP;

	[Header("Contadores, carpetas y Vector3")]
	public GameObject Carpeta;

	public Vector3 pos;
	public int contador_id = 0;
	public int contador_Size = 0;
	public int contador_index = 0;
	public int contador_Grids = 0;

	GameObject CarpetaVacia;

	[Header("Instanciamiento de Bomberos")]
	public GameObject[] Bomberos = new GameObject[5];



	Class_Paredes paredes_lista;

	// IEnumerator - yield return
	IEnumerator SendData(string data)
    {
		WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";

		using (UnityWebRequest www = UnityWebRequest.Post(url, form))        
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
            }
            else
            {
				//Le quitamos los espacios vacios para convertir a Json
                string jsonString = www.downloadHandler.text.Replace('\'', '\"');

				//Guardado del Json en la clase Class_Paredes
				paredes_lista = JsonUtility.FromJson<Class_Paredes>(jsonString);
				string paredes_string = JsonUtility.ToJson(paredes_lista);

				Invoke("LeerID", 1f);
			}
		}

    }

    // Start is called before the first frame update
    void Start()
    {
		Fin_Juego.SetActive(false);
		VerMapa.SetActive(false);
		Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        StartCoroutine(SendData(json));

		//Generamos una carpeta para instanciar los prefabs ahi
		CarpetaVacia = Instantiate(Carpeta, transform.position, Quaternion.identity);
	}

	//Leemos el ID para identificar el evento al que corresponden las listas
	public void LeerID()
    {
		try
			
		{
			Debug.Log("Paso");
			Debug.Log(paredes_lista.ID[contador_id]);

			if (paredes_lista.ID[contador_id] == -3)
			{
				contador_id++;
				Invoke("Generar_Bomberos", 1f);
			}
			else if (paredes_lista.ID[contador_id] == -2)
			{
				contador_id++;
				Invoke("Generar_Entorno", 1f);
			}
			else if (paredes_lista.ID[contador_id] == -1)
			{
				contador_id++;
				Invoke("Generar_Paredes", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 0)
			{
				contador_id++;
				Invoke("CrearHumo", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 1)
			{
				contador_id++;
				Invoke("PrendeFuego", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 2)
			{
				contador_id++;
				Invoke("MoverBombero", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 3)
			{
				contador_id++;
				Invoke("ExtinguirFuegoHumo", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 4)
			{
				contador_id++;
				Invoke("ActualizarMuro", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 5)
			{
				contador_id++;
				Invoke("BomberoCargando", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 6)
			{
				contador_id++;
				Invoke("RomperUsar", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 7)
			{
				contador_id++;
				Invoke("EliminarIP", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 8)
			{
				contador_id++;
				Invoke("CrearIP", 1f);
			}
			else if (paredes_lista.ID[contador_id] == 9)
			{
				contador_id++;
				Invoke("DescubreIP", 1f);
			}
		}
		catch (Exception e)
		{
			Fin_Juego.SetActive(true);
			VerMapa.SetActive(true);
			print("Final del codigo");
		}
		
	}

	//Genera el escenario con las paredes, puertas y entradas
	public void Generar_Paredes()
	{
		//Creamos una lista que contiene el tamanio de la grid en eje x, y, & numero de esquinas
		int[] lista_indices;
		lista_indices = new int[paredes_lista.Size[contador_Size]];

		for (int index = 0; index < ((paredes_lista.Size[contador_Size])); index++) {
			lista_indices[index] = paredes_lista.Index[contador_index];
			contador_index++;
		}
		contador_Size++;

		//Numero de posiciones en y = 6
		int val_paredes_i = lista_indices[0];

		//Numero de posiciones en x = 8
		int val_paredes_j = lista_indices[1];

		//Numero de posibles esquinas para la pared = 4
		int val_paredes_k = lista_indices[2];

		//Se itera la grid entera en orden empezando por la esquina superior ezquierda
		for (int i = 0; i < val_paredes_i; i++)
		{
			for (int j = 0; j < val_paredes_j; j++)
			{
				for (int k = 0; k < val_paredes_k; k++)
				{
					if (paredes_lista.Grids[contador_Grids] != 0)
					{

						//Sacamos la rotacion del objeto
						pos = new Vector3(j * 5f, 1f, i * 5f); //Se ajusta la posicion al entorno de Unity
						float rotacionY = 0f;


						if (k == 0)
						{
							//Arriba
							rotacionY = 90f;
							pos.z = pos.z - 2f;
						}
						else if (k == 1)
						{
							//Izquierda
							rotacionY = 0f;
							pos.x = pos.x - 2f;
						}
						else if (k == 2)
						{
							//Abajo
							rotacionY = 90f;
							pos.z = pos.z + 2f;
						}
						else if (k == 3)
						{
							//Derecha
							rotacionY = 0f;
							pos.x = pos.x + 2f;
						}

						//Instanciamos el objeto correspondiente al numero
						Vector3 rotationVector = new Vector3(0, rotacionY, 0);
						Quaternion rotation = Quaternion.Euler(rotationVector);

						if (paredes_lista.Grids[contador_Grids] == 1)
						{
							//Pared
							Instantiate(pared, pos, rotation, CarpetaVacia.transform);
                        }
                        else if (paredes_lista.Grids[contador_Grids] == 4)
                        {
							///Puerta Casa
                            Instantiate(puerta, pos, rotation, CarpetaVacia.transform);
                        }
                        else if (paredes_lista.Grids[contador_Grids] == 6)
						{
							//Puerta_Entrada
							Instantiate(puerta_entrada, pos, rotation, CarpetaVacia.transform);
						}
					}
					contador_Grids++;
				}
			}
		}

		LeerID();
	}

	public void Generar_Entorno()
	{
		//Recorremos la matriz en orden para generar las entidades
		int contador_i = paredes_lista.Index[contador_index];
		contador_index++;

		int contador_j = paredes_lista.Index[contador_index];
		contador_index++;

		contador_Size++;

		for (int i = 0; i < contador_i; i++)
		{
			for (int j = 0; j < contador_j; j++)
			{
				if (paredes_lista.Grids[contador_Grids] != 0)
				{
					pos = new Vector3(j * 5f, 1f, i * 5f); //Se ajusta la posicion al entorno de Unity

					Vector3 rotationVector = new Vector3(0, 180, 0);
					Quaternion rotation = Quaternion.Euler(rotationVector);

					if (paredes_lista.Grids[contador_Grids] == 1)
					{
						//Humo
						rotationVector = new Vector3(270, 0, 0);
						rotation = Quaternion.Euler(rotationVector);
						Instantiate(humo, pos, rotation, CarpetaVacia.transform);
					}

					if (paredes_lista.Grids[contador_Grids] == 2)
					{
						//Fuego
						Instantiate(fuego, pos, rotation, CarpetaVacia.transform);
					}
					if (paredes_lista.Grids[contador_Grids] == 4 || paredes_lista.Grids[contador_Grids] == 5)
					{
						//Puntos de Interes
						Debug.Log("CrearPuntosInteres");
						Instantiate(puntoInteres, pos, rotation, CarpetaVacia.transform);
					}
				}
				contador_Grids++;
			}
		}
		LeerID();
	}

	public void Generar_Bomberos()
    {
		//Recuperamos los ejes e id del bombero a generar
		int i= paredes_lista.Index[contador_index];
		contador_index++;

		int j = paredes_lista.Index[contador_index];
		contador_index++;

		int id = paredes_lista.Index[contador_index]; //Son un total de 6 Bomberos
		contador_index++;

		pos = new Vector3(j * 5f, 1f, i * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 180, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);

		Bomberos[id] = Instantiate(bombero, pos, rotation); //Se guarda la instancia en el arreglo de Bomberos

		contador_Size++;
		LeerID();
	}

	public void CrearHumo()
	{
		//Recuperamos los ejes del humo
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity


		Vector3 rotationVector = new Vector3(270, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(humo, pos, rotation, CarpetaVacia.transform);

		contador_Size++;
		LeerID();
	}

	public void PrendeFuego()
	{
		//Recuperamos los ejes del fuego
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(fuego, pos, rotation, CarpetaVacia.transform);

		contador_Size++;
		LeerID();
	}

	public void MoverBombero()
    {
		//Recuperamos los ejes del movimiento del Bombero y su id
		int x_move = paredes_lista.Index[contador_index] * 5; //Se ajusta la posicion al entorno de Unity
		contador_index++;

		int y_move = paredes_lista.Index[contador_index] * 5; //Se ajusta la posicion al entorno de Unity
		contador_index++;

		int id = paredes_lista.Index[contador_index];
		contador_index++;

		Debug.Log(x_move);
		Debug.Log(y_move);
		Debug.Log(id);

		PlayerMovement script_Bomberos = Bomberos[id].GetComponent<PlayerMovement>(); //Pasamos los ejes al bombero
		script_Bomberos.x_towards = x_move;
		script_Bomberos.y_towards = y_move;
		script_Bomberos.movimiento = true;

		contador_Size++;
		LeerID();
	}

	public void ExtinguirFuegoHumo()
	{
		//Recuperamos los ejes del fuego a extinguir
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(destruir_humo_fuego, pos, rotation, CarpetaVacia.transform); //destruir_humo elimina el fuego/humo y se autodestruye

		contador_Size++;
		LeerID();
	}

	public void ActualizarMuro()
	{
		//Recuperamos los ejes de la pared y su id de rotacion
		int x = paredes_lista.Index[contador_index];
		int y = paredes_lista.Index[contador_index + 1];
		int k = paredes_lista.Index[contador_index + 2];

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		//Sacamos el desplazamiento del objeto
		if (k == 0)
		{
			pos.z = pos.z - 2f;
		}
		else if (k == 1)
		{
			pos.x = pos.x - 2f;
		}
		else if (k == 2)
		{
			pos.z = pos.z + 2f;
		}
		else if (k == 3)
		{
			pos.x = pos.x + 2f;
		}

		//destruirMuro elimina la pared/puerta y se autodestruye
		Instantiate(destruirMuro, pos, Quaternion.identity, CarpetaVacia.transform); 

		Invoke("ConstruirMuro", 0.2f);
	}

	public void ConstruirMuro()
    {
		//Recuperamos los ejes de la pared, id de rotacion y vida
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		int k = paredes_lista.Index[contador_index];
		contador_index++;

		int vidas = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity


		float rotacionY = 0f;

		//Sacamos el desplazamiento y rotacion del objeto
		if (k == 0)
		{
			rotacionY = 90f;
			pos.z = pos.z - 2f;
		}
		else if (k == 1)
		{
			rotacionY = 0f;
			pos.x = pos.x - 2f;
		}
		else if (k == 2)
		{
			rotacionY = 90f;
			pos.z = pos.z + 2f;
		}
		else if (k == 3)
		{
			rotacionY = 0f;
			pos.x = pos.x + 2f;
		}

		Vector3 rotationVector = new Vector3(0, rotacionY, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);


		//Dependiendo de la vida se genera el muro Daniado o Destruido
		if(vidas == 2)
        {
			Instantiate(paredDaniada, pos, rotation, CarpetaVacia.transform);
		}
		if (vidas == 3)
		{
			Instantiate(paredDestruida, pos, rotation, CarpetaVacia.transform);
		}

		contador_Size++;
		LeerID();
	}

	public void BomberoCargando()
	{
		//Recuperamos la id del bombero
		int id = paredes_lista.Index[contador_index];
		contador_index++;

		//Activamos/Desactivamos a su hijo Victima dependiendo del estado
		GameObject playerRescued = Bomberos[id].transform.GetChild(0).gameObject;
		if (playerRescued.GetComponent<Activado>().estado_Activado == 0)
		{
			playerRescued.SetActive(true);
			playerRescued.GetComponent<Activado>().estado_Activado = 1;
		}
		else
		{
			playerRescued.GetComponent<Activado>().estado_Activado = 0;
			playerRescued.SetActive(false);
		}

		contador_Size++;
		LeerID();
	}

	public void RomperUsar()
	{
		//Recuperamos la id del bombero
		int id = paredes_lista.Index[contador_index];
		contador_index++;

		//Activamos el trigger de la animacion de pateando
		Bomberos[id].GetComponent<PlayerMovement>().Pateando();

		contador_Size++;
		LeerID();
	}

	public void EliminarIP()
	{
		//Recuperamos los ejes del IP a eliminar
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);

		//destruirIP elimina el IP y se autodestruye
		Instantiate(destruirIP, pos, rotation, CarpetaVacia.transform);

		contador_Size++;
		LeerID();
	}
	public void CrearIP()
	{
		//Recuperamos los ejes del IP
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);

		Instantiate(puntoInteres, pos, rotation, CarpetaVacia.transform);

		contador_Size++;
		LeerID();
	}
	public void DescubreIP()
	{
		//Recuperamos los ejes del IP a descubrir
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f); //Se ajusta la posicion al entorno de Unity

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);

		//Se crea el efecto de Victima
		Instantiate(DescubrirIP, pos, rotation, CarpetaVacia.transform);

		contador_Size++;
		LeerID();
	}
}

 [System.Serializable]
public class Class_Paredes
{
	public int[] Grids;
	public int[] Index;
	public int[] Size;
	public int[] ID;
}