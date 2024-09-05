using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{

    public float runSpeed = 7;
    public float rotateSpeed = 250;
    public int x_towards;
    public int y_towards;
    public bool movimiento = false;

    public float res_x;
    public float res_y;

    public Rigidbody rb;
    public Animator animator;

    public float x, y;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        x = Input.GetAxis("Horizontal");
        y = Input.GetAxis("Vertical");

        transform.Translate(x * Time.deltaTime * runSpeed, 0, y * Time.deltaTime * runSpeed);

        if (movimiento)
        {
            Vector3 objetivo = new Vector3(x_towards, 0, y_towards);
            var step = runSpeed * Time.deltaTime;

            transform.position = Vector3.MoveTowards(transform.position, objetivo, step);
            res_x = transform.position.x - objetivo.x;
            res_y = transform.position.y - objetivo.y;

            animator.SetFloat("VelX", res_x);
            animator.SetFloat("VelY", res_y);
            if (transform.position.x == x_towards && transform.position.y == y_towards)
            {
                rb.velocity = new Vector3(0f, 0f, 0f);
                movimiento = false;
            }
        }

    }

    public void Pateando()
    {
        animator.SetTrigger("Patear");
    }

}
