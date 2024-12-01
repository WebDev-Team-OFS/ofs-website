import axios from 'axios'
import React from 'react'

export const checkLoginHelper = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8080/api/protected', {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            }  // Ensures cookies (including session cookies) are sent with the request
        });
        console.log("logged in");
        return true;
       
    }
    catch (error) {
        try{
            const response = await axios.post('http://127.0.0.1:8080/api/refresh',{}, {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("refresh_token")}`
                }  // Ensures cookies (including session cookies) are sent with the request
            });
            if (response.data.access_token) {
                localStorage.setItem("access_token", response.data.access_token)
                console.log("REFRESHED YIPPEE!!")
                return true
                
            }
            else {
                return false
            }
        }
        catch (error) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            console.log("EXPIRED");
            console.error("Error response:", error.response);
            return false
        }
    }
}