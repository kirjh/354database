document.addEventListener("DOMContentLoaded", () => {
    
    // document.cookie = "user_id=; Path=/"
    console.log(document.cookie)
    console.log(document.cookie.split("; ").find((row) => row.startsWith("user_id="))?.split("=")[1])
});