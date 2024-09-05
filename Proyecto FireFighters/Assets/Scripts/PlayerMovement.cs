using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [Header("Movimiento")]
    public int x_towards;
    public int y_towards;
    public float runSpeed = 7;
    public bool movimiento = false;

    [Header("Animador y RigidBody")]
    public Rigidbody rb;
    public Animator animator;

    // Obtenemos el RigidBody
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        //Si esta en movimiento entonces nos movemos hacia la nueva posicion
        if (movimiento)
        {
            Vector3 objetivo = new Vector3(x_towards, 0, y_towards);
            var step = runSpeed * Time.deltaTime;

            transform.position = Vector3.MoveTowards(transform.position, objetivo, step);
            float res_x = transform.position.x - objetivo.x;
            float res_y = transform.position.y - objetivo.y;

            animator.SetFloat("VelX", res_x);
            animator.SetFloat("VelY", res_y);

            //Cuando estemos en la posicion deseada entonces se para el movimiento y velocidad
            if (transform.position.x == x_towards && transform.position.y == y_towards)
            {
                rb.velocity = new Vector3(0f, 0f, 0f);
                movimiento = false;
            }
        }

    }

    //Mandamos Animacion de Patear
    public void Pateando()
    {
        animator.SetTrigger("Patear");
    }

}
