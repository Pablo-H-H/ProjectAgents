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

public class WebClient : MonoBehaviour
{

	string jsonString;
    public GameObject pared;
	public GameObject paredDaniada;
	public GameObject paredDestruida;
	public GameObject puerta;
	public GameObject amarillo;
	public GameObject DescubrirIP;

	public GameObject humo;
	public GameObject fuego;
	public GameObject bombero;
	public GameObject destruir_humo_fuego;

	public GameObject puntoInteres;
	public GameObject BomberoCarga;
	public GameObject BomberoAtaca;
	public GameObject destruirMuro;
	public GameObject destruirIP;
	public GameObject moverBombero;

	public GameObject Carpeta;
	//public Quaternion rotacion;
	public Vector3 pos;
	int[,,] pos_Age;

	public int contador_id = 0;
	public int contador_tamanio = 0;
	public int contador_index = 0;
	public int contador_combine_grids = 0;

	GameObject CarpetaVacia;

	int contador_steps;


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
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
				Debug.Log(www.downloadHandler.text.Replace('\'', '\"'));
                jsonString = www.downloadHandler.text.Replace('\'', '\"');


				paredes_lista = JsonUtility.FromJson<Class_Paredes>(jsonString);

				string paredes_string = JsonUtility.ToJson(paredes_lista);

				//var resultado = (from lista in paredes_lista.Paredes select lista);

				Invoke("LeerID", 1f);
				
				

			}
		}

    }

    // Start is called before the first frame update
    void Start()
    {
		contador_steps = 0;
		//string call = "What's up?";
		Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        //StartCoroutine(SendData(call));
        StartCoroutine(SendData(json));
        // transform.localPosition
    }

    // Update is called once per frame
    void Update()
    {

    }

	public void LeerID()
    {
		if(paredes_lista.ID[contador_id] == -1)
        {
			contador_id++;
			Invoke("Generar_Paredes", 1.5f);
        }
		else if (paredes_lista.ID[contador_id] == -2)
		{
			contador_id++;
			Invoke("Generar_BomberoYEntorno", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 0)
		{
			contador_id++;
			Invoke("CrearHumo", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 1)
		{
			contador_id++;
			Invoke("PrendeFuego", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 2)
		{
			contador_id++;
			Invoke("MoverBombero", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 4)
		{
			contador_id++;
			Invoke("ActualizarMuro", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 5)
		{
			contador_id++;
			Invoke("BomberoCargando", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 6)
		{
			contador_id++;
			Invoke("RomperUsar", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 7)
		{
			contador_id++;
			Invoke("EliminarIP", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 8)
		{
			contador_id++;
			Invoke("CrearIP", 1.5f);
		}
		else if (paredes_lista.ID[contador_id] == 9)
		{
			contador_id++;
			Invoke("DescubreIP", 1.5f);
		}





	}

	public void Generar_Paredes()
	{

		CarpetaVacia = Instantiate(Carpeta, transform.position, Quaternion.identity);
		int[] lista_indices;
		lista_indices = new int[paredes_lista.Tamanio[contador_tamanio]];

		for (int index = 0; index < ((paredes_lista.Tamanio[contador_tamanio])); index++) {
			lista_indices[index] = paredes_lista.Index[contador_index];
			Debug.Log(contador_index);
			contador_index++;
		}
		contador_tamanio++;

		int pos_i;
		pos_i = lista_indices[0];
		Debug.Log(pos_i);
		int val_paredes_i = pos_i;

		int pos_j;
		pos_j = lista_indices[1];
		Debug.Log(pos_j);			
		int val_paredes_j = pos_j;

		int pos_k;
		pos_k = lista_indices[2];
		Debug.Log(pos_k);			
		int val_paredes_k = pos_k;

		for (int i = 0; i < val_paredes_i; i++)
		{
			for (int j = 0; j < val_paredes_j; j++)
			{
				for (int k = 0; k < val_paredes_k; k++)
				{

					if (paredes_lista.Combine_grids[contador_combine_grids] != 0)
					{
						pos = new Vector3(j * 5f, 1f, i * 5f);
						//rotacion = Quaternion.Euler(0,0,0);
						float rotacionY = 0f;


						if (k == 0)
						{
							rotacionY = 90f;
							pos.z = pos.z - 2f;
						}

						if (k == 1)
						{
							rotacionY = 0f;
							pos.x = pos.x + 2f;
						}

						if (k == 2)
						{
							rotacionY = 90f;
							pos.z = pos.z + 2f;
						}

						if (k == 3)
						{
							rotacionY = 0f;
							pos.x = pos.x - 2f;
						}

						Vector3 rotationVector = new Vector3(0, rotacionY, 0);
						Quaternion rotation = Quaternion.Euler(rotationVector);

						if (paredes_lista.Combine_grids[contador_combine_grids] == 1)
						{
							Instantiate(pared, pos, rotation, CarpetaVacia.transform);
						}

						if (paredes_lista.Combine_grids[contador_combine_grids] == 6)
						{
							Instantiate(puerta, pos, rotation, CarpetaVacia.transform);
						}

						if (paredes_lista.Combine_grids[contador_combine_grids] == 4)
						{
							Instantiate(amarillo, pos, rotation, CarpetaVacia.transform);
						}


					}

					contador_combine_grids++;
					Debug.Log(contador_combine_grids);

				}
			}
		}
		LeerID();
	}

	public void Generar_BomberoYEntorno()
	{
		int count = 0;

		int contador_i;
		contador_i = paredes_lista.Index[contador_index];
		contador_index++;

		int contador_j;
		contador_j = paredes_lista.Index[contador_index];
		contador_index++;

		contador_tamanio++;



		for (int i = 0; i < contador_i; i++)
		{
			for (int j = 0; j < contador_j; j++)
			{


				if (paredes_lista.Combine_grids[contador_combine_grids] != 0)
				{
					pos = new Vector3(j * 5f, 1f, i * 5f);
					//rotacion = Quaternion.Euler(0,0,0);

					Vector3 rotationVector = new Vector3(0, 180, 0);
					Quaternion rotation = Quaternion.Euler(rotationVector);

					if (paredes_lista.Combine_grids[contador_combine_grids] == 1)
					{
						rotationVector = new Vector3(270, 0, 0);
						rotation = Quaternion.Euler(rotationVector);
						Debug.Log("CrearHumo");
						Instantiate(humo, pos, rotation, CarpetaVacia.transform);
					}

					if (paredes_lista.Combine_grids[contador_combine_grids] == 2)
					{
						Debug.Log("CrearFuego");
						Instantiate(fuego, pos, rotation, CarpetaVacia.transform);
					}

					if (paredes_lista.Combine_grids[contador_combine_grids] == 3)
					{
						Debug.Log("CrearBombero");
						Instantiate(bombero, pos, rotation, CarpetaVacia.transform);
					}
					if (paredes_lista.Combine_grids[contador_combine_grids] == 4 || paredes_lista.Combine_grids[contador_combine_grids] == 5)
					{
						Debug.Log("CrearBombero");
						Instantiate(puntoInteres, pos, rotation, CarpetaVacia.transform);
					}

				}

				contador_combine_grids++;
			}
		}

		contador_steps++;
		LeerID();
	}

	public void CrearHumo()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(270, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearHumo");
		Instantiate(humo, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}

	public void PrendeFuego()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(270, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearFuego");
		Instantiate(fuego, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}

	public void MoverBombero()
    {
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int x_move = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y_move = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearParaMover");
		GameObject Bombero = Instantiate(moverBombero, pos, rotation, CarpetaVacia.transform);
		Bombero.GetComponent<MovePlayer>().x = x_move;
		Bombero.GetComponent<MovePlayer>().y = y_move;

		contador_tamanio++;
		LeerID();
	}

	public void ExtinguirFuegoHumo()
	{
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(destruir_humo_fuego, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}

	public void ActualizarMuro()
	{
		int x = paredes_lista.Index[contador_index];

		int y = paredes_lista.Index[contador_index + 1];

		int k = paredes_lista.Index[contador_index + 2];

		pos = new Vector3(x * 5f, 1f, y * 5f);

		//rotacion = Quaternion.Euler(0,0,0);
		float rotacionY = 0f;


		if (k == 0)
		{
			rotacionY = 90f;
			pos.z = pos.z - 2f;
		}

		if (k == 1)
		{
			rotacionY = 0f;
			pos.x = pos.x + 2f;
		}

		if (k == 2)
		{
			rotacionY = 90f;
			pos.z = pos.z + 2f;
		}

		if (k == 3)
		{
			rotacionY = 0f;
			pos.x = pos.x - 2f;
		}


		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearDestructor");
		Instantiate(destruirMuro, pos, rotation, CarpetaVacia.transform);
		Invoke("ConstruirMuro", 0.2f);
	}

	public void ConstruirMuro()
    {
		int x = paredes_lista.Index[contador_index];
		contador_index++;

		int y = paredes_lista.Index[contador_index];
		contador_index++;

		int k = paredes_lista.Index[contador_index];
		contador_index++;

		int vidas = paredes_lista.Index[contador_index];
		contador_index++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		//rotacion = Quaternion.Euler(0,0,0);
		float rotacionY = 0f;


		if (k == 0)
		{
			rotacionY = 90f;
			pos.z = pos.z - 2f;
		}

		if (k == 1)
		{
			rotacionY = 0f;
			pos.x = pos.x + 2f;
		}

		if (k == 2)
		{
			rotacionY = 90f;
			pos.z = pos.z + 2f;
		}

		if (k == 3)
		{
			rotacionY = 0f;
			pos.x = pos.x - 2f;
		}

		Vector3 rotationVector = new Vector3(0, rotacionY, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);


		Debug.Log("CrearDestructor");
		if(vidas == 2)
        {
			Instantiate(paredDaniada, pos, rotation, CarpetaVacia.transform);
		}
		if (vidas == 3)
		{
			Instantiate(paredDestruida, pos, rotation, CarpetaVacia.transform);
		}

		contador_tamanio++;
		LeerID();
	}

	public void BomberoCargando()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearFuego");
		Instantiate(BomberoCarga, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}

	public void RomperUsar()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearFuego");
		Instantiate(BomberoAtaca, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}

	public void EliminarIP()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Debug.Log("CrearFuego");
		Instantiate(destruirIP, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}
	public void CrearIP()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(puntoInteres, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}
	public void DescubreIP()
	{
		int x = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		int y = paredes_lista.Combine_grids[contador_combine_grids];
		contador_combine_grids++;

		pos = new Vector3(x * 5f, 1f, y * 5f);

		Vector3 rotationVector = new Vector3(0, 0, 0);
		Quaternion rotation = Quaternion.Euler(rotationVector);
		Instantiate(DescubrirIP, pos, rotation, CarpetaVacia.transform);

		contador_tamanio++;
		LeerID();
	}
	

}



 [System.Serializable]
public class Class_Paredes
{
	public int[] Combine_grids;
	public int[] Index;
	public int[] Tamanio;
	public int[] ID;
}