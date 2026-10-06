import {useState } from "react"
import VidInput from "./VidInput/VidInput.jsx"
function App() {
  const [videoFile, setVideoFile] = useState()
  const [inferenceData, setInferenceData] = useState()
  const [loading, setLoading] = useState(false)
  const BASE_URL = "http://0.0.0.0:8000/"
  /* 
    the goal:
      - to be able to update a video to the backend
      - retrieve the returned files as images and display the images

      1) create an input field to take video from file system || done
      2) create an endpoint to send the file to the backend
      3) create a dto to grab the returned files
      4) parse the returned files into a component
  */

  const handleOnClick = () => {
    getInference(videoFile)
  }
  const getInference = async (videoFile) => {
    const videoData = new FormData()
    videoData.append('video', videoFile)

    try {
      setLoading(true)
      const response = await fetch(BASE_URL+"video", {
        method:"POST",
        body: videoData
      })
      if (!response.ok) {
        throw new Error("eruh") 
      }

      const data = await response.json()
      setLoading(false)
      setInferenceData(data)
      console.log("data fetched very good")
    }catch(error) {
      console.error("eruh")
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <>
      <VidInput setVideoFile={setVideoFile}></VidInput>
      <button
        onClick={handleOnClick}>Touch me</button>
      {loading ? <h1>loading...</h1> : <h1></h1> }
    </>
  )
}

export default App
