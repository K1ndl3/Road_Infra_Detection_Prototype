import "./VidInput.css"

function VidInput({setVideoFile}) {

    const handleOnChange = (event) => {
        setVideoFile(event.target.files[0])
    }

    return (<>
        <div className="video-input-container">
            <h1>two pipelines in app.py. One trained on kaggle with 50 epochs, the losses are in the notebook. The other is an API call to roboflow</h1>
            <input type="file"
                accept="video/*"
                onChange={handleOnChange} />

        </div>
    </>)
}

export default VidInput