import "./VidInput.css"

function VidInput({setVideoFile}) {

    const handleOnChange = (event) => {
        setVideoFile(event.target.files[0])
    }

    return (<>
        <div className="video-input-container">
            <h1>Gimme video cuzzo</h1>
            <input type="file"
                accept="video/*"
                onChange={handleOnChange} />

        </div>
    </>)
}

export default VidInput