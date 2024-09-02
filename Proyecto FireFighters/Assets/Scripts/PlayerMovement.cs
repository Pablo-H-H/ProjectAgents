using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{

    public float runSpeed = 7;
    public float rotateSpeed = 250;

    public Animator animator;

    public float x, y;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        x = Input.GetAxis("Horizontal");
        y = Input.GetAxis("Vertical");

        transform.Translate(x * Time.deltaTime * runSpeed, 0, y * Time.deltaTime * runSpeed);

        animator.SetFloat("VelX", x);
        animator.SetFloat("VelY", y);

        if (Input.GetKeyDown(KeyCode.P))
        {
            animator.SetTrigger("Patear");
        }

        if (Input.GetKeyDown(KeyCode.O))
        {
            animator.SetTrigger("Danio");
        }

    }
}
