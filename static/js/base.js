
//add expense
const addExpenseForm = document.getElementById('addExpenseForm')
if (addExpenseForm){
    addExpenseForm.addEventListener('submit',async function(event){
        event.preventDefault()
        const form = event.target
        const formData = new FormData(form)
        const data = Object.fromEntries(formData.entries())

        //Build payload
        const payload = {
            'amount':parseFloat(data.amount),
            'title':data.title
        }

        //Check authentication
        try{
            const token = getCookie('access_token')
            if(!token){
                throw new Error('Authentication token not found');
            }
            const response = await fetch('/expenses/',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body:JSON.stringify(payload)
            })

            if (response.ok){
                window.location.href =  ('/expenses/expenses-page')
            }

            else{
                const errorData = response.json();
                alert(`Error:${errorData.message}`);
            }

        }
        catch(error){
            console.error('Error:',error);
            alert('An error occurred, try again later.');
        }
    })
}


// Register logic
const registerForm = document.getElementById('registerForm');
if (registerForm){
    registerForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password1 !== data.password2) {
            alert('Passwords do not match');
            return;
        }
        const payload = {
            user_name: data.username,
            email: data.email,
            first_name: data.first_name,
            last_name: data.last_name,
            password: data.password1,
            role: data.role
        };

        console.log(payload)
        try {
            const response = await fetch('/users/',{
                method : 'POST',
                headers :{
                    'Content-Type': 'application/json'
                } ,
                body: JSON.stringify(payload)
                });

            if (response.ok){
                window.location.href = '/home-page'
            }

            else{
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }

        }
        catch(error){
            console.error('Error:',error);
            alert('Error, please try again later!');
        }
    }
);
}

// Login
const loginForm = document.getElementById('loginForm')
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
            event.preventDefault()
            console.log('login js is running')
            const form
                = event.target;
            const formData = new FormData(form);

            const payload = new URLSearchParams();

            for (const [key, value] of formData.entries()) {
                payload.append(key, value);
            }
            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });
                if (response.ok) {
                    // const data = await response.json()
                    // document.cookie = `access_token=${data.access_token};path=/;`
                    window.location.href = '/expenses/expenses-page';
                    console.log('the response is ok')

                } else {
                    const errorData = response.json()
                    alert(`Error:${errorData.message}`)
                }
            } catch (error) {
                console.log({'Error': error});
                alert('Error Please try again!');
            }

        }
    )
}
// Edit Expenses

const editExpenseForm = document.getElementById('editExpenseForm')
if (editExpenseForm){
    console.log('hello')
    editExpenseForm.addEventListener('submit',async function(event){
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries())
        console.log(data)
        var url = window.location.pathname;
        const ExpenseId = url.substring(url.lastIndexOf('/')+1);

        const payload = {
            title:data.title,
            amount:parseFloat(data.amount)
        };

        try{
            const token = getCookie('access_token');
            console.log(token);

            if (!token){
                throw new Error('Authentication token not found');
            }
            const response = await fetch(`/expenses/update/${ExpenseId}`,{
                method:'PUT',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body:JSON.stringify(payload)
            });

            if (response.ok){
                window.location.href = ('/expenses/expenses-page');

            }
            else{
                //Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }
        }
        catch(error){
            console.error('Error:',error);
            alert('An error occurred, try again later');
        }



    })


    document.getElementById('deleteExpense').addEventListener('click',async function(){
        var url = window.location.pathname
        const expenseId = url.substring(url.lastIndexOf('/')+1)

        try{
            const token = getCookie('access_token')
            if (!token){
                throw new Error('Authentication Token not found');
            }

            const response = await fetch(`/expenses/delete/${expenseId}`,{
                method:'DELETE',
                headers:
                    {
                        'Authorization': `Bearer ${token}`
                    }

            })

            if (response.ok){
                window.location.href = ('/expenses/expenses-page')
            }
            else{
                const errorData = response.json()
                alert(`Error:${errorData.detail}`)
            }

        }
        catch(error){
            console.error('Error:',error)
            alert('An error occurred. Please try again.')
        }
    })
}




function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function logout() {
        // Get all cookies
        const cookies = document.cookie.split(";");

        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }

        // Redirect to the login page
        window.location.href = '/auth/login-page';
    };



//Helper function to get cookie by name

// function getCookie(name){
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== ''){
//         const cookies = document.cookie.split(';')
//         for(let i =0; i < cookies.length; i++){
//             const cookie = cookies[i].trim();
//             if(cookie.substring(0,name.length + 1) === (name + '=') ){
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1,));
//                 break;
//             }
//         }
//     }
//     return cookieValue
// };


