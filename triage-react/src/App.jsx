import { useState } from 'react'

function App() {
  const [name, setName] = useState('')
  const [age, setAge] = useState('')
  const [symptoms, setSymptoms] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const newErrors = {}
    if (!name) newErrors.name = 'Name is required'
    if (!age) newErrors.age = 'Age is required'
    if (age < 1 || age > 120) newErrors.age = 'Age must be between 1 and 120'
    if (!symptoms) newErrors.symptoms = 'Symptoms are required'
    if (symptoms.length < 10) newErrors.symptoms = 'Please describe symptoms in more detail'
    return newErrors
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const newErrors = validate()
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    setErrors({})
    setSubmitted(true)
  }

  const handleReset = () => {
    setName('')
    setAge('')
    setSymptoms('')
    setSubmitted(false)
    setErrors({})
  }

  return (
    <div style={{
      maxWidth: '500px',
      margin: '40px auto',
      padding: '24px',
      fontFamily: 'Arial',
      background: '#1e293b',
      borderRadius: '12px',
      color: '#e2e8f0'
    }}>
      <h1>🚑 Patient Form</h1>

      {!submitted ? (
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '6px' }}>
              Patient Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '6px',
                border: errors.name ? '1px solid red' : '1px solid #334155',
                background: '#0f172a',
                color: '#e2e8f0'
              }}
            />
            {errors.name && (
              <p style={{ color: 'red', fontSize: '12px', marginTop: '4px' }}>
                {errors.name}
              </p>
            )}
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '6px' }}>Age</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '6px',
                border: errors.age ? '1px solid red' : '1px solid #334155',
                background: '#0f172a',
                color: '#e2e8f0'
              }}
            />
            {errors.age && (
              <p style={{ color: 'red', fontSize: '12px', marginTop: '4px' }}>
                {errors.age}
              </p>
            )}
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '6px' }}>
              Symptoms
            </label>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '6px',
                border: errors.symptoms ? '1px solid red' : '1px solid #334155',
                background: '#0f172a',
                color: '#e2e8f0',
                height: '100px'
              }}
            />
            {errors.symptoms && (
              <p style={{ color: 'red', fontSize: '12px', marginTop: '4px' }}>
                {errors.symptoms}
              </p>
            )}
          </div>

          <button
            type="submit"
            style={{
              width: '100%',
              padding: '12px',
              background: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '16px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Submit
          </button>
        </form>
      ) : (
        <div>
          <h2 style={{ color: '#22c55e' }}>✅ Submitted Successfully</h2>
          <p>Name: {name}</p>
          <p>Age: {age}</p>
          <p>Symptoms: {symptoms}</p>
          <button
            onClick={handleReset}
            style={{
              marginTop: '16px',
              padding: '10px 20px',
              background: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Submit Another
          </button>
        </div>
      )}
    </div>
  )
}

export default App