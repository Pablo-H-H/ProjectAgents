using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Diagnostics;
using Debug = UnityEngine.Debug;


public class JSONDemo : MonoBehaviour
{
	string path;
	string jsonString;

	void Start()
	{
		path = Application.streamingAssetsPath + "/Creature.json";
		jsonString = File.ReadAllText(path);
		Creature Yumo = JsonUtility.FromJson<Creature>(jsonString);
		//Debug.Log(Yumo);

		string Yumo_string = JsonUtility.ToJson(Yumo);
		//Debug.Log(Yumo_string);
	}
}

 [System.Serializable]
public class Creature
{
	public string Name;
	public int Level;
	public int[] Stats;
}