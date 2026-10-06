function FrameCards({ frames }) {
  if (!frames?.length) {
    return null
  }

  return (
    <div className="frame-cards">
      {frames.map((frame) => (
        <div key={frame.index} className="frame-card">
          <p>Frame {frame.index}</p>
          <img
            src={`data:image/jpeg;base64,${frame.image_base64}`}
            alt={`Annotated frame ${frame.index}`}
          />
        </div>
      ))}
    </div>
  )
}

export default FrameCards
