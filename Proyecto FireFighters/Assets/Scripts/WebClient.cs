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
    public GameObject puerta;
	public GameObject amarillo;
	//public Quaternion rotacion;
	public Vector3 pos;
	int[,,] pos_Paredes;

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
                jsonString = www.downloadHandler.text.Replace('\'', '\"');

				paredes_lista = JsonUtility.FromJson<Class_Paredes>(jsonString);

				//var resultado = (from lista in paredes_lista.Paredes select lista);

				string paredes_string = JsonUtility.ToJson(paredes_lista);

				Invoke("Generar_Paredes", 1f);

			}
		}

    }

    // Start is called before the first frame update
    void Start()
    {
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

	public void Generar_Paredes()
	{
		int count = 0;
		pos_Paredes = new int[6, 8, 4];

		for (int i = 0; i < 6; i++)
		{
			for (int j = 0; j < 8; j++)
			{
				for (int k = 0; k < 4; k++)
				{
					pos_Paredes[i, j, k] = paredes_lista.Paredes[count];

					if (paredes_lista.Paredes[count] != 0)
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

						if (paredes_lista.Paredes[count] == 1)
						{
							Instantiate(pared, pos, rotation);
						}

						if (paredes_lista.Paredes[count] == 6)
						{
							Instantiate(puerta, pos, rotation);
						}

						if (paredes_lista.Paredes[count] == 4)
						{
							Instantiate(amarillo, pos, rotation);
						}


					}

					count++;

				}
			}
		}
	}
}

 [System.Serializable]
public class Class_Paredes
{
	public int[] Paredes;
}