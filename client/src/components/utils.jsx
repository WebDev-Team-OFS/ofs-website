import axios from 'axios'


export const checkLoginHelper = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8080/api/protected', {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }  
        });
        return true;
       
    }
    catch (error) {
        try{
            const response = await axios.post('http://127.0.0.1:8080/api/refresh',{}, {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("refresh_token")}`
                }  
            });
            if (response.data.access_token) {
                localStorage.setItem("access_token", response.data.access_token)
                return true
                
            }
            else {
                return false
            }
        }
        catch (error) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            return false
        }
    }
}

export const checkAdminLoginHelper = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8080/api/admin/protected', {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
            }  
        });
        return true;
       
    }
    catch (error) {
        try{
            const response = await axios.post('http://127.0.0.1:8080/api/refresh',{}, {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("admin_refresh_token")}`
                }  
            });
            if (response.data.access_token) {
                localStorage.setItem("access_token", response.data.access_token)
                return true
                
            }
            else {
                return false
            }
        }
        catch (error) {
            localStorage.removeItem("admin_access_token");
            localStorage.removeItem("admin_refresh_token");
            return false
        }
    }
}
