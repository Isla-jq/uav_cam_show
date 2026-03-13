const uav1_but_cli = document.querySelector("#uav1_but")
const uav2_but_cli = document.querySelector("#uav2_but")

uav1_but_cli.addEventListener("click", async (event) => {
    try {
        const response = await axios.post('/api/click-event', {
            timestamp : event.timeStamp,
            entity_name: "uav1_button"
        })
    }
    catch (error){
        console.error('请求失败:', error);
    }
});
uav2_but_cli.addEventListener("click", async (event) => {
    try {
    const response = await axios.post('/api/click-event', {
            timestamp : event.timeStamp,
            entity_name: "uav2_button"
        })
    }
    catch (error){
        console.error('请求失败:', error);
    }
})