import { useState, useEffect, useRef } from 'react'
import './App.css'
import cropHero1 from './assets/crop-hero-1.jpg'
import translationsModule from './translations'

const translations = translationsModule?.translations || translationsModule

const initialFormData = {
  season: 'monsoon',
  cropName: 'maize',
  soilType: 'loam',
  temperature: 27,
  rainfall: 650,
  humidity: 70,
  nitrogen: 110,
  phosphorus: 45,
  potassium: 40
}

const cropOptions = [
  'wheat',
  'maize',
  'paddy',
  'cotton',
  'sugarcane',
  'chickpea',
  'groundnut',
  'millet',
  'soybean',
  'barley',
  'tomato',
  'potato',
  'mustard',
  'sesame',
  'sunflower'
]

const languageOptions = [
  { value: 'en', label: 'English' },
  { value: 'hi', label: 'हिंदी' },
  { value: 'te', label: 'తెలుగు' },
  { value: 'ta', label: 'தமிழ்' },
  { value: 'bn', label: 'বাংলা' },
  { value: 'mr', label: 'मराठी' }
]

const VALIDATION_RULES = {
  season: { required: true, minLength: 2, messageKey: 'errorMessageRequired' },
  cropName: { required: true, minLength: 2, messageKey: 'errorCropNameMinLength' },
  soilType: { required: true, messageKey: 'errorSoilTypeRequired' },
  temperature: { required: true, min: -50, max: 60, messageKey: 'errorTemperatureRange' },
  rainfall: { required: true, min: 0, max: 10000, messageKey: 'errorRainfallRange' },
  humidity: { required: true, min: 0, max: 100, messageKey: 'errorHumidityRange' },
  nitrogen: { required: true, min: 0, max: 500, messageKey: 'errorNitrogenRange' },
  phosphorus: { required: true, min: 0, max: 500, messageKey: 'errorPhosphorusRange' },
  potassium: { required: true, min: 0, max: 500, messageKey: 'errorPotassiumRange' }
}

const validateFormData = (data, t) => {
  const errors = {}
  Object.keys(VALIDATION_RULES).forEach((field) => {
    const rule = VALIDATION_RULES[field]
    const value = data[field]

    if (rule.required && (value === '' || value === null || value === undefined)) {
      errors[field] = t?.validationMessages?.[rule.messageKey] || t.errorMessageRequired || 'This field is required'
      return
    }

    if (typeof value === 'number') {
      if (rule.min !== undefined && value < rule.min) {
        errors[field] = t?.validationMessages?.[rule.messageKey] || t.errorMessageRequired || 'This field is required'
        return
      }
      if (rule.max !== undefined && value > rule.max) {
        errors[field] = t?.validationMessages?.[rule.messageKey] || t.errorMessageRequired || 'This field is required'
        return
      }
    }

    if (typeof value === 'string' && rule.minLength && value.length < rule.minLength) {
      errors[field] = t?.validationMessages?.[rule.messageKey] || t.errorMessageRequired || 'This field is required'
    }
  })
  return errors
}

const heroImageUrls = {
  large: 'https://images.stockcake.com/public/5/a/5/5a56acb9-d7da-4c70-a121-4128968caeef_large/vibrant-crop-rows-stockcake.jpg',
  small1: 'https://source.unsplash.com/featured/800x600?crops',
  small2: 'https://getfarms.in/assets/images/blog/top-ten-profitable-agriculture-business-ideas-successful-farming.webp',
  full: 'https://mytanfarms.com/wp-content/uploads/2024/12/which-farming-is-most-profitable-in-india.webp'
}

const handleHeroImageError = (event) => {
  event.currentTarget.onerror = null
  event.currentTarget.src = cropHero1
}

function ChatbotWidget({ language }) {
  const API_URL = import.meta.env.VITE_API_URL || ''
  const t = translations[language] || translations.en
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { id: 1, text: t.chatWelcome, sender: 'bot' }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  useEffect(() => {
    setMessages([{ id: Date.now(), text: t.chatWelcome, sender: 'bot' }])
  }, [t.chatWelcome])

  const quickActions = [
    { label: t.quickActionFertilizer, query: 'What fertilizer plan should I use for wheat during monsoon?' },
    { label: t.quickActionSoil, query: 'How can I improve my soil health?' },
    { label: t.quickActionIrrigation, query: 'When is the best time to water crops this season?' },
    { label: t.quickActionPests, query: 'How do I protect my field from common pests?' }
  ]

  const handleClearChat = () => {
    setMessages([{ id: Date.now(), text: t.chatWelcome, sender: 'bot' }])
  }

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return

    const userId = Date.now()
    const userMsg = { id: userId, text: messageText, sender: 'user' }
    setMessages((prev) => [...prev, userMsg])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText, language })
      })

      const data = await response.json()
      if (data.success) {
        const botMsg = {
          id: Date.now() + 1,
          text: data.reply || "I couldn't generate a response. Please try again.",
          sender: 'bot'
        }
        setMessages((prev) => [...prev, botMsg])
      } else {
        const errorMsg = {
          id: Date.now() + 1,
          text: `Error: ${data.error || 'Unable to process your message'}`,
          sender: 'bot'
        }
        setMessages((prev) => [...prev, errorMsg])
      }
    } catch (error) {
      const errorMsg = {
        id: Date.now() + 1,
        text: `${t.connectionErrorPrefix} ${error.message}`,
        sender: 'bot'
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuickAction = (query) => {
    handleSendMessage(query)
  }

  const panelContent = (
    <div className="chat-panel" onClick={(e) => e.stopPropagation()}>
      <div className="chat-panel-header">
        <div className="chat-header-title">
          <span className="robot-icon">🤖</span>
          <div>
            <strong>{t.chatbotName}</strong>
            <p>{t.chatDescription}</p>
          </div>
        </div>
        <div className="chat-header-actions">
          <button className="secondary-btn" onClick={handleClearChat}>{t.clear}</button>
          <button className="secondary-btn" onClick={() => setIsOpen(false)}>{t.close}</button>
        </div>
      </div>

      <div className="chat-panel-body">
        <div className="chat-panel-note">{t.chatWelcome}</div>
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message message-${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          {isLoading && <div className="message message-bot">{t.predicting}</div>}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-suggestions">
          {quickActions.map((action) => (
            <button
              key={action.label}
              type="button"
              className="quick-action"
              onClick={() => handleQuickAction(action.query)}
            >
              {action.label}
            </button>
          ))}
        </div>

        <div className="chat-input-area">
          <input
            type="text"
            className="chat-input"
            placeholder={t.chatPlaceholder}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !isLoading) {
                handleSendMessage(inputMessage)
              }
            }}
            disabled={isLoading}
          />
          <button
            className="send-btn primary-btn"
            onClick={() => handleSendMessage(inputMessage)}
            disabled={isLoading || !inputMessage.trim()}
          >
            {t.send}
          </button>
        </div>
      </div>
    </div>
  )

  return (
    <>
      <button
        className="chat-panel-button"
        aria-label={t.openAiChatAssistant}
        onClick={() => setIsOpen(true)}
      >
        <span className="robot-icon">🤖</span>
        <span>{t.askAi}</span>
      </button>

      {isOpen && (
        <div className="chat-panel-overlay" onClick={() => setIsOpen(false)}>
          {panelContent}
        </div>
      )}
    </>
  )
}

function App() {
  const API_URL = import.meta.env.VITE_API_URL || ''
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [formData, setFormData] = useState(initialFormData)
  const [predictionResult, setPredictionResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [formErrors, setFormErrors] = useState({})
  const t = translations[selectedLanguage] || translations.en
  const heroSmartPlanningItems = t.heroSmartPlanningItems?.split(';') || []

  useEffect(() => {
    const browserLang = navigator.language?.split('-')[0]
    if (translations[browserLang]) {
      setSelectedLanguage(browserLang)
    }
  }, [])

  useEffect(() => {
    document.documentElement.lang = selectedLanguage
  }, [selectedLanguage])

  useEffect(() => {
    document.title = t.pageTitle || 'AgriPredict'
    const descriptionMeta = document.querySelector('meta[name="description"]')
    if (descriptionMeta) {
      descriptionMeta.setAttribute('content', t.pageDescription || 'AgriPredict - AI-powered crop yield assistant')
    }
  }, [t])

  const getCropLabel = (cropKey) => {
    const key = String(cropKey || '').trim().toLowerCase()
    return (
      translations[selectedLanguage]?.crops?.[key] ||
      translations.en?.crops?.[key] ||
      key
    )
  }

  const getSoilLabel = (soilKey) => {
    const key = String(soilKey || '').trim().toLowerCase()
    return (
      translations[selectedLanguage]?.soilTypes?.[key] ||
      translations.en?.soilTypes?.[key] ||
      key
    )
  }

  const handleFormChange = (event) => {
    const { name, value, type } = event.target
    setFormData((current) => ({
      ...current,
      [name]: type === 'number' ? parseFloat(value) : value
    }))

    if (formErrors[name]) {
      setFormErrors((prev) => {
        const updated = { ...prev }
        delete updated[name]
        return updated
      })
    }
  }

  const handlePredict = async (event) => {
    event.preventDefault()

    const errors = validateFormData(formData, t)
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors)
      return
    }

    setFormErrors({})
    setLoading(true)
    setPredictionResult(null)

    try {
      const apiPayload = {
        season: formData.season,
        crop_type: formData.cropName,
        soil_type: formData.soilType,
        temperature: formData.temperature,
        rainfall: formData.rainfall,
        humidity: formData.humidity,
        nitrogen: formData.nitrogen,
        phosphorus: formData.phosphorus,
        potassium: formData.potassium,
        language: selectedLanguage
      }

      const response = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiPayload)
      })

      const data = await response.json()
      if (!response.ok || !data.success) {
        throw new Error(data.error || t.defaultPredictionError)
      }

      setPredictionResult({
        predictedYield: data.yield_ton_per_ha ?? data.predicted_yield ?? '--',
        confidence: data.confidence_score ?? data.confidence ?? 85,
        modelType: data.model_type ?? 'Ensemble (Multiple AI Models)',
        modelBreakdown: data.model_breakdown ?? null,
        recommendations: data.recommendations ?? [
          'Monitor soil moisture weekly',
          'Apply balanced NPK fertilizer',
          'Time irrigation around peak growth'
        ],
        details: {
          cropName: data.crop_display_name || data.crop_name || getCropLabel(formData.cropName),
          soilType: getSoilLabel(formData.soilType),
          rainfall: formData.rainfall,
          cropKey: formData.cropName
        }
      })
    } catch (error) {
      setPredictionResult({ error: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <nav className="topbar">
        <div className="brand-bar">
          <div className="brand-mark">AP</div>
          <div className="brand-copy">
            <strong>{t.title}</strong>
            <span>{t.subtitle}</span>
          </div>
        </div>

        <ul className="nav-links">
          <li><a href="#home">{t.home}</a></li>
          <li><a href="#predictor">{t.predictor}</a></li>
          <li><a href="#contact">{t.contact}</a></li>
        </ul>

        <div className="nav-actions-right">
          <label className="lang-switch">
            <span>{t.language}</span>
            <select
              value={selectedLanguage}
              onChange={(event) => setSelectedLanguage(event.target.value)}
              className="lang-select"
            >
              {languageOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <button
            type="button"
            className="nav-action"
            onClick={() => document.getElementById('predictor')?.scrollIntoView({ behavior: 'smooth' })}
          >
            {t.predictNow}
          </button>
        </div>
      </nav>

      <main className="main-panel">
        <section className="hero-section" id="home">
          <article className="hero-copy">
            <span className="eyebrow">{t.eyebrow}</span>
            <h1>{t.heroTitle}</h1>
            <p>{t.heroSubtitle}</p>

            <div className="hero-actions">
              <button
                type="button"
                className="primary-btn"
                onClick={() => document.getElementById('predictor')?.scrollIntoView({ behavior: 'smooth' })}
              >
                {t.predictNow}
              </button>
            </div>

            <div className="hero-hint">{t.heroHint}</div>

            <div className="pill-row" aria-label="Supported crops">
              {cropOptions.slice(0, 8).map((crop) => (
                <span key={crop} className="pill-badge">
                  {getCropLabel(crop)}
                </span>
              ))}
            </div>

            <div className="hero-media-grid">
              <div className="hero-media-large">
                <img
                  src={heroImageUrls.small2}
                  alt={t.heroImageAltSmall2}
                  onError={handleHeroImageError}
                />
              </div>

              <div className="hero-media-small-grid">
                <div className="hero-media-small">
                  <img
                    src={heroImageUrls.large}
                    alt={t.heroImageAltLarge}
                    onError={handleHeroImageError}
                  />
                  <p>{t.heroImageCaption1}</p>
                </div>

                <div className="hero-media-small">
                  <img
                    src={heroImageUrls.small1}
                    alt={t.heroImageAltSmall1}
                    onError={handleHeroImageError}
                  />
                  <p>{t.heroImageCaption2}</p>
                </div>
              </div>
            </div>

            <div className="hero-fill-card">
              <div>
                <span className="hero-fill-label">{t.heroSmartPlanning}</span>
                <h3>{t.heroFieldReadyAi}</h3>
              </div>
              <ul>
                {heroSmartPlanningItems.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="stat-grid">
              <div className="stat-block">
                <strong>98%</strong>
                <span>Model Trust Score</span>
              </div>
              <div className="stat-block">
                <strong>120K+</strong>
                <span>Field Predictions</span>
              </div>
              <div className="stat-block">
                <strong>24/7</strong>
                <span>Operational Insights</span>
              </div>
            </div>
          </article>

          <aside className="hero-panel glass-card">
            <div className="panel-header">
              <span>{t.heroFieldReadyAi}</span>
              <strong>{t.heroGrowWithConfidence}</strong>
            </div>
            <div className="panel-details">
              <p>{t.heroActionableRecommendations}</p>
              <ul className="panel-list">
                <li>{t.heroYieldEstimates}</li>
                <li>{t.heroSoilNutrient}</li>
                <li>{t.heroAdaptiveIrrigation}</li>
              </ul>
            </div>
            <div className="panel-foot">
              <span className="panel-chip">{t.heroDesignedFor}</span>
            </div>
          </aside>
        </section>

        <section className="feature-strip">
          <article className="feature-card">
            <h3>{t.heroFeatureSmartInputs}</h3>
            <p>{t.heroFeatureSmartInputsDesc}</p>
          </article>
          <article className="feature-card">
            <h3>{t.heroFeatureDecisionEngine}</h3>
            <p>{t.heroFeatureDecisionEngineDesc}</p>
          </article>
          <article className="feature-card">
            <h3>{t.heroFeatureFarmAnalytics}</h3>
            <p>{t.heroFeatureFarmAnalyticsDesc}</p>
          </article>
        </section>

        <section className="predictor-section" id="predictor">
          <div className="section-header">
            <div>
              <span className="section-label">{t.predictor}</span>
              <h2>{t.predictorSectionTitle}</h2>
            </div>
            <p>{t.heroPredictorIntro}</p>
          </div>

          <div className="predictor-visual-grid">
            <article className="predictor-visual-card">
              <img
                src={heroImageUrls.large}
                alt={t.heroImageAltLarge}
                onError={handleHeroImageError}
              />
              <p>{t.heroImageCaption1}</p>
            </article>

            <article className="predictor-visual-card">
              <img
                src={heroImageUrls.full}
                alt={t.heroImageAltSmall2}
                onError={handleHeroImageError}
              />
              <p>{t.heroImageCaption2}</p>
            </article>
          </div>

          <div className="predict-grid">
            <form className="form-card glass-card" onSubmit={handlePredict}>
              <div className="field-grid">
                <label>
                  {t.season}
                  <select
                    name="season"
                    value={formData.season}
                    onChange={handleFormChange}
                    className={formErrors.season ? 'input-error' : ''}
                    aria-label={t.season}
                  >
                    <option value="monsoon">{t.seasonMonsoon}</option>
                    <option value="spring">{t.seasonSpring}</option>
                    <option value="summer">{t.seasonSummer}</option>
                    <option value="winter">{t.seasonWinter}</option>
                  </select>
                  {formErrors.season && <span className="error-msg">{formErrors.season}</span>}
                </label>

                <label>
                  {t.cropType}
                  <select
                    name="cropName"
                    value={formData.cropName}
                    onChange={handleFormChange}
                    className={formErrors.cropName ? 'input-error' : ''}
                    aria-label={t.cropType}
                  >
                    {cropOptions.map((crop) => (
                      <option key={crop} value={crop}>
                        {getCropLabel(crop)}
                      </option>
                    ))}
                  </select>
                  {formErrors.cropName && <span className="error-msg">{formErrors.cropName}</span>}
                </label>

                <label>
                  {t.soilType}
                  <select
                    name="soilType"
                    value={formData.soilType}
                    onChange={handleFormChange}
                    className={formErrors.soilType ? 'input-error' : ''}
                    aria-label={t.soilType}
                  >
                    <option value="loam">{t.soilLoam}</option>
                    <option value="clay">{t.soilClay}</option>
                    <option value="sandy">{t.soilSandy}</option>
                    <option value="silt">{t.soilSilt}</option>
                  </select>
                  {formErrors.soilType && <span className="error-msg">{formErrors.soilType}</span>}
                </label>

                <label>
                  {t.temperature}
                  <input
                    type="number"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleFormChange}
                    className={formErrors.temperature ? 'input-error' : ''}
                    min="-50"
                    max="60"
                    step="0.1"
                    placeholder={t.temperature}
                    aria-label={t.temperature}
                  />
                  {formErrors.temperature && <span className="error-msg">{formErrors.temperature}</span>}
                </label>

                <label>
                  {t.rainfall}
                  <input
                    type="number"
                    name="rainfall"
                    value={formData.rainfall}
                    onChange={handleFormChange}
                    className={formErrors.rainfall ? 'input-error' : ''}
                    min="0"
                    max="10000"
                    step="1"
                    placeholder={t.rainfall}
                    aria-label={t.rainfall}
                  />
                  {formErrors.rainfall && <span className="error-msg">{formErrors.rainfall}</span>}
                </label>

                <label>
                  {t.humidity}
                  <input
                    type="number"
                    name="humidity"
                    value={formData.humidity}
                    onChange={handleFormChange}
                    className={formErrors.humidity ? 'input-error' : ''}
                    min="0"
                    max="100"
                    step="0.1"
                    placeholder={t.humidity}
                    aria-label={t.humidity}
                  />
                  {formErrors.humidity && <span className="error-msg">{formErrors.humidity}</span>}
                </label>

                <label>
                  {t.nitrogen}
                  <input
                    type="number"
                    name="nitrogen"
                    value={formData.nitrogen}
                    onChange={handleFormChange}
                    className={formErrors.nitrogen ? 'input-error' : ''}
                    min="0"
                    max="500"
                    step="1"
                    placeholder={t.nitrogen}
                    aria-label={t.nitrogen}
                  />
                  {formErrors.nitrogen && <span className="error-msg">{formErrors.nitrogen}</span>}
                </label>

                <label>
                  {t.phosphorus}
                  <input
                    type="number"
                    name="phosphorus"
                    value={formData.phosphorus}
                    onChange={handleFormChange}
                    className={formErrors.phosphorus ? 'input-error' : ''}
                    min="0"
                    max="500"
                    step="1"
                    placeholder={t.phosphorus}
                    aria-label={t.phosphorus}
                  />
                  {formErrors.phosphorus && <span className="error-msg">{formErrors.phosphorus}</span>}
                </label>

                <label>
                  {t.potassium}
                  <input
                    type="number"
                    name="potassium"
                    value={formData.potassium}
                    onChange={handleFormChange}
                    className={formErrors.potassium ? 'input-error' : ''}
                    min="0"
                    max="500"
                    step="1"
                    placeholder={t.potassium}
                    aria-label={t.potassium}
                  />
                  {formErrors.potassium && <span className="error-msg">{formErrors.potassium}</span>}
                </label>
              </div>

              <button type="submit" className="primary-btn" disabled={loading}>
                {loading ? t.predicting : t.predictButton}
              </button>
            </form>

            <aside className="result-card glass-card">
              <div className="result-header">
                <span>{t.resultsHeading}</span>
                <strong>{t.resultSubheading}</strong>
              </div>

              {predictionResult && !predictionResult.error ? (
                <div className="result-content">
                  <div className="result-metric">
                    <span>{t.predictedYield}</span>
                    <strong>{predictionResult.predictedYield} t/ha</strong>
                  </div>

                  <div className="result-metric">
                    <span>{t.confidence}</span>
                    <strong>{predictionResult.confidence}%</strong>
                  </div>

                  <div className="result-metric model-info">
                    <span>{t.modelLabel}</span>
                    <strong>{predictionResult.modelType}</strong>
                  </div>

                  {predictionResult.modelBreakdown && (
                    <div className="model-breakdown">
                      <h4>{t.modelBreakdown}</h4>
                      <ul>
                        {Object.entries(predictionResult.modelBreakdown).map(([name, value]) => (
                          <li key={name}>
                            <strong>{name}</strong>: {value !== null ? `${value} t/ha` : t.notAvailable || 'N/A'}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="recommendations">
                    <h4>{t.recommendations}</h4>
                    <ul>
                      {predictionResult.recommendations.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="detail-grid">
                    <div>
                      <span>{t.cropType}</span>
                      <strong>{predictionResult.details.cropName}</strong>
                    </div>
                    <div>
                      <span>{t.soilType}</span>
                      <strong>{predictionResult.details.soilType}</strong>
                    </div>
                    <div>
                      <span>{t.rainfall}</span>
                      <strong>{predictionResult.details.rainfall} mm</strong>
                    </div>
                  </div>
                </div>
              ) : predictionResult?.error ? (
                <div className="result-empty">
                  <p className="error-display">{predictionResult.error}</p>
                </div>
              ) : null}
            </aside>
          </div>
        </section>

        <section className="contact-section" id="contact">
          <div className="contact-cta glass-card">
            <div className="section-header">
              <div>
                <span className="section-label">{t.contact}</span>
                <h2>{t.contactTitle}</h2>
              </div>
              <p>{t.contactSubtitle}</p>
            </div>

            <div className="contact-grid">
              <article className="contact-card">
                <strong>{t.support}</strong>
                <p>
                  {t.contactEmailText} <a href="mailto:support@agripredict.com">support@agripredict.com</a>
                </p>
              </article>

              <article className="contact-card">
                <strong>{t.contactFieldInsights}</strong>
                <p>{t.contactFieldInsightsDesc}</p>
              </article>
            </div>
          </div>
        </section>
      </main>

      <ChatbotWidget language={selectedLanguage} />
    </div>
  )
}

export default App
