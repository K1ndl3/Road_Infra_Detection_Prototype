import { useState } from "react"
import VidInput from "./VidInput/VidInput.jsx"
import FrameCards from "./FrameCards/FrameCards.jsx"

function App() {
  const [videoFile, setVideoFile] = useState()
  const [inferenceData, setInferenceData] = useState()
  const [loading, setLoading] = useState(false)
  const BASE_URL = "http://localhost:8000/"

  const handleOnClick = () => {
    if (!videoFile) return
    getInference(videoFile)
  }

  const getInference = async (videoFile) => {
    const videoData = new FormData()
    videoData.append("file", videoFile)

    try {
      setLoading(true)
      const response = await fetch(BASE_URL + "detect", {
        method: "POST",
        body: videoData,
      })
      if (!response.ok) {
        throw new Error("eruh")
      }

      const data = await response.json()
      setInferenceData(data)
      console.log("data fetched very good")
    } catch (error) {
      console.error("eruh", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <VidInput setVideoFile={setVideoFile}></VidInput>
      <button onClick={handleOnClick}>Touch me</button>
      {loading ? <h1>loading...</h1> : null}
      <FrameCards frames={inferenceData?.frames} />
    </>
  )
}

export default App
