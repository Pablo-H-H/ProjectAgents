using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovePlayer : MonoBehaviour
{
    GameObject player;
    public int x;
    public int y;
    public float runSpeed;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Player")
        {
            player = other.gameObject;
            player.GetComponent<PlayerMovement>().x_towards = x;
            player.GetComponent<PlayerMovement>().y_towards = y;
            player.GetComponent<PlayerMovement>().movimiento = true;

        }
    }

    public void MoverseHacia()
    {
        transform.Translate(x * Time.deltaTime * runSpeed, 0, y * Time.deltaTime * runSpeed);
    }

}
