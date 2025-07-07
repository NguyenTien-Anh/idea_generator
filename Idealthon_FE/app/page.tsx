"use client"

import type React from "react"
import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Progress } from "@/components/ui/progress"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { useApi } from "@/hooks/use-api"
import { toast } from "sonner"
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { FrontendTranscriptItem, FrontendIdeaItem } from "@/lib/api"
import {
  Cloud,
  FileText,
  Download,
  Lightbulb,
  Sparkles,
  Search,
  User,
  Archive,
  Palette,
  Globe,
  Smartphone,
  Bell,
  Film,
  Mic,
  ArrowLeft,
  AlertCircle,
  AlertTriangle,
  Loader2,
  Copy,
  X,
  Check,
} from "lucide-react"

export default function Component() {
  const [selectedRole, setSelectedRole] = useState<"editor" | "creator">("editor")
  const [selectedAudioLanguage, setSelectedAudioLanguage] = useState("auto")
  const [uploadProgress, setUploadProgress] = useState(0)
  const [showTranscript, setShowTranscript] = useState(false)
  const [showIdeas, setShowIdeas] = useState(false)
  const [showContentModal, setShowContentModal] = useState(false)
  const [selectedContentType, setSelectedContentType] = useState<string>("")
  const [searchQuery, setSearchQuery] = useState("")
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const [generatedContent, setGeneratedContent] = useState<string>("")
  const [selectedIdeaId, setSelectedIdeaId] = useState<number | null>(null)
  const [selectedIdea, setSelectedIdea] = useState<FrontendIdeaItem | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [copied, setCopied] = useState(false)

  // State for tracking sub idea selections for each idea
  const [subIdeaSelections, setSubIdeaSelections] = useState<Record<number, Record<string, boolean>>>({})

  // API hook for backend integration
  const {
    loadingStates,
    errorStates,
    uploadAudio,
    generateIdeasFromTranscript,
    generateContentFromIdea,
    clearError,
  } = useApi()

  // File input ref for programmatic access
  const fileInputRef = useRef<HTMLInputElement>(null)

  // State for transcript and idea data
  const [transcriptData, setTranscriptData] = useState<FrontendTranscriptItem[]>([])
  const [ideaData, setIdeaData] = useState<FrontendIdeaItem[]>([])

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    // Validate file type
    if (!file.type.startsWith('audio/')) {
      toast.error('Please upload an audio file')
      return
    }

    setUploadedFile(file)
    setUploadProgress(0)

    // Simulate upload progress
    let progress = 0
    const progressInterval = setInterval(() => {
      progress += 10
      setUploadProgress(progress)
      if (progress >= 100) {
        clearInterval(progressInterval)
      }
    }, 200)

    toast.success(`File "${file.name}" uploaded successfully`)
  }

  const handleGenerateTranscript = async () => {
    if (!uploadedFile) {
      toast.error('Please upload an audio file first')
      return
    }

    clearError('uploadError')

    try {
      const result = await uploadAudio(uploadedFile, selectedAudioLanguage)
      if (result) {
        setTranscriptData(result)
        setShowTranscript(true)
        toast.success('Transcript generated successfully!')
      }
    } catch (error) {
      // Error is already handled by the useApi hook
      console.error('Failed to generate transcript:', error)
    }
  }

  const toggleTranscriptRemove = (id: number) => {
    setTranscriptData((prev) => prev.map((item) => (item.id === id ? { ...item, removed: !item.removed } : item)))
  }

  const updateIdeaFormat = (id: number, format: string) => {
    setIdeaData((prev) => prev.map((item) => (item.id === id ? { ...item, format } : item)))
  }

  // Handle sub idea selection toggle
  const toggleSubIdeaSelection = (ideaId: number, subIdeaId: string) => {
    setSubIdeaSelections(prev => ({
      ...prev,
      [ideaId]: {
        ...prev[ideaId],
        [subIdeaId]: !prev[ideaId]?.[subIdeaId]
      }
    }))
  }

  // Initialize sub idea selections when idea data changes
  const initializeSubIdeaSelections = (ideas: FrontendIdeaItem[]) => {
    const initialSelections: Record<number, Record<string, boolean>> = {}
    ideas.forEach(idea => {
      initialSelections[idea.id] = {}
      idea.subIdeas.forEach(subIdea => {
        initialSelections[idea.id][subIdea.id] = subIdea.selected
      })
    })
    setSubIdeaSelections(initialSelections)
  }

  // Get selected sub ideas for a specific idea
  const getSelectedSubIdeas = (ideaId: number): string[] => {
    const idea = ideaData.find(item => item.id === ideaId)
    if (!idea) return []

    return idea.subIdeas
      .filter(subIdea => subIdeaSelections[ideaId]?.[subIdea.id] !== false)
      .map(subIdea => subIdea.text)
  }

  const handleIdeaSelection = (ideaId: string) => {
    const id = parseInt(ideaId)
    setSelectedIdeaId(id)
    const idea = ideaData.find(item => item.id === id)
    setSelectedIdea(idea || null)
  }

  const resetSelection = () => {
    setSelectedIdeaId(null)
    setSelectedIdea(null)
    setGeneratedContent("")
  }

  const handleBackToIdeas = () => {
    setShowIdeas(true)
    setShowContentModal(false)
    // Keep the selection when going back
  }

  const handleGenerateIdeas = async () => {
    if (transcriptData.length === 0) {
      toast.error('No transcript data available. Please generate a transcript first.')
      return
    }

    const nonRemovedItems = transcriptData.filter(item => !item.removed)
    if (nonRemovedItems.length === 0) {
      toast.error('Please ensure at least one transcript item is not removed.')
      return
    }

    clearError('ideasError')

    // Reset previous selections when generating new ideas
    resetSelection()

    try {
      const result = await generateIdeasFromTranscript(transcriptData)
      if (result) {
        setIdeaData(result)
        initializeSubIdeaSelections(result) // Initialize sub idea selections
        setShowIdeas(true)
        setShowTranscript(false)
        toast.success(`${result.length} ideas generated successfully!`)
      }
    } catch (error) {
      console.error('Failed to generate ideas:', error)
    }
  }

  const handleGenerateContent = async () => {
    if (!selectedIdea) {
      toast.error('Please select an idea first')
      return
    }

    clearError('contentError')

    try {
      // Get only selected sub ideas for content generation
      const selectedSubIdeas = getSelectedSubIdeas(selectedIdea.id)
      const subIdeasText = selectedSubIdeas.length > 0 ? selectedSubIdeas.join('. ') : ''

      // Create a more detailed idea text with only selected sub ideas
      const ideaText = `${selectedIdea.mainIdea}. ${subIdeasText}`

      const result = await generateContentFromIdea(
        selectedIdea.format.toLowerCase(),
        ideaText.trim(),
        selectedSubIdeas
      )
      if (result) {
        setGeneratedContent(result)
        setShowContentModal(true)
        setShowIdeas(false)
        toast.success(`${selectedIdea.format} content generated successfully!`)
      } else {
        toast.error('Failed to generate content. Please try again.')
      }
    } catch (error) {
      console.error('Failed to generate content:', error)
      toast.error('An error occurred while generating content.')
    }
  }

  const handleNewContentGeneration = () => {
    setGeneratedContent("")
    setShowContentModal(false)
    setShowIdeas(true)
    resetSelection()
  }

  const handleCopyContent = async () => {
    if (!generatedContent) return

    try {
      await navigator.clipboard.writeText(generatedContent)
      setCopied(true)
      toast.success('Content copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast.error('Failed to copy content')
    }
  }



  const getContentPreview = (type: string) => {
    switch (type) {
      case "Video":
        return {
          title: "Video Script",
          content: `[INTRO - 0:00-0:10]
Hook: "What if I told you that 25 minutes could transform your entire workday?"

[MAIN CONTENT - 0:10-2:30]
• Introduce the Pomodoro Technique
• Explain the science behind focused work sessions
• Show practical implementation steps
• Share success stories and statistics

[CALL TO ACTION - 2:30-3:00]
"Try this technique today and let us know your results in the comments below!"

[OUTRO - 3:00-3:15]
Subscribe for more productivity tips and techniques.`,
        }
      case "Blog":
        return {
          title: "Blog Article",
          content: `# Mastering Productivity: The Science Behind Deep Work

## Introduction
In our hyperconnected world, the ability to focus deeply has become a superpower. Today, we'll explore proven strategies that can transform your work efficiency.

## The Pomodoro Technique: Your Focus Foundation
The Pomodoro Technique isn't just a time management method—it's a scientifically-backed approach to maintaining peak concentration.

### How It Works:
1. Choose a task to focus on
2. Set a timer for 25 minutes
3. Work with complete focus until the timer rings
4. Take a 5-minute break
5. Repeat the cycle

## The Science Behind Deep Work
Research shows that our brains can maintain peak focus for approximately 25-45 minutes before requiring a break. This aligns perfectly with the Pomodoro intervals.

## Conclusion
Implementing these techniques consistently can lead to a 40% increase in productivity within just two weeks of practice.`,
        }
      case "Post":
        return {
          title: "Social Media Post",
          content: `🚀 PRODUCTIVITY GAME-CHANGER ALERT! 🚀

Just discovered the secret to 10x focus: The Pomodoro Technique! 🍅

✨ 25 minutes of deep work
✨ 5-minute break
✨ Repeat & watch magic happen

I've been using this for 2 weeks and my productivity has SKYROCKETED! 📈

Who else is ready to transform their workday? Drop a 🍅 if you're in!

#ProductivityHacks #DeepWork #PomodoroTechnique #WorkSmart #FocusMode #ProductivityTips #TimeManagement #WorkFromHome #Efficiency #SuccessMindset`,
        }
      case "Infographic":
        return {
          title: "Infographic Content",
          content: `📊 POMODORO TECHNIQUE INFOGRAPHIC

🎯 THE METHOD:
• 25 min focused work
• 5 min break
• Repeat 4 cycles
• 30 min long break

📈 THE BENEFITS:
• 40% productivity increase
• Reduced mental fatigue
• Better work-life balance
• Enhanced creativity

🧠 THE SCIENCE:
• Matches natural attention spans
• Prevents cognitive overload
• Maintains peak performance
• Builds sustainable habits

💡 PRO TIPS:
• Turn off notifications
• Choose one task per session
• Use a physical timer
• Track your progress

🏆 SUCCESS RATE: 87% of users report improved focus within 1 week`,
        }
      default:
        return { title: "Content Preview", content: "Select a format to see content preview." }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 font-sans">
      {/* Background Pattern */}
      <div
        className="fixed inset-0 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fillRule='evenodd'%3E%3Cg fill='%239C92AC' fillOpacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      {/* Header */}
      <header className="relative z-10 p-6">
        <div className="max-w-7xl mx-auto">
          <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl headline-enhanced">Audio Ideas Generator</h1>
                  <p className="text-slate-600 font-medium">Discover a treasure of ideas from audio</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500" />
                  <Input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 w-64 bg-white/40 backdrop-blur-xl border-white/30 rounded-2xl"
                  />
                </div>
                <Button className="w-12 h-12 bg-white/30 backdrop-blur-xl border-white/20 rounded-2xl p-0 btn-blue-hover">
                  <Bell className="w-5 h-5 text-slate-700" />
                </Button>
                <Button className="w-12 h-12 bg-white/30 backdrop-blur-xl border-white/20 rounded-2xl p-0 btn-blue-hover">
                  <User className="w-5 h-5 text-slate-700" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 p-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Featured Card */}
            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-0 rounded-3xl p-8 text-white shadow-2xl">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 bg-purple-500 rounded-3xl flex items-center justify-center">
                  <FileText className="w-8 h-8" />
                </div>
                <div>
                  <h2 className="text-4xl font-bold mb-2 text-white">Audio Ideas</h2>
                  <p className="text-white/80 text-lg font-medium">AI-powered content generation from your audio</p>
                </div>
              </div>
              <div className="text-white/50 text-sm">Ready to transform your content</div>
            </Card>

            {/* Role Selector */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-4 headline-enhanced">Who are you?</h3>
              <div className="flex gap-4">
                {["editor", "creator"].map((role) => (
                  <Button
                    key={role}
                    onClick={() => setSelectedRole(role as "editor" | "creator")}
                    className={`flex-1 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 ${
                      selectedRole === role
                        ? "bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg shadow-purple-500/25"
                        : "bg-white/40 backdrop-blur-xl text-slate-700 border border-white/30 btn-blue-hover"
                    }`}
                  >
                    {role.charAt(0).toUpperCase() + role.slice(1)}
                  </Button>
                ))}
              </div>
            </Card>

            {/* Upload Section */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-8 shadow-xl">
              <div className="relative group">
                <input
                  type="file"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="border-2 border-dashed border-slate-300 rounded-3xl p-12 transition-all duration-300 group-hover:border-purple-400 group-hover:bg-white/10 bg-white/5 backdrop-blur-xl">
                  <div className="flex flex-col items-center space-y-4">
                    <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-blue-500 rounded-3xl flex items-center justify-center shadow-lg">
                      <Mic className="w-10 h-10 text-white" />
                    </div>
                    <div className="text-center">
                      <h3 className="text-2xl font-semibold text-slate-700 mb-2 headline-enhanced">Upload Audio File</h3>
                      <p className="text-slate-500">Drag and drop your audio file here or click to browse</p>
                    </div>
                  </div>
                </div>
                {uploadProgress > 0 && (
                  <div className="mt-6">
                    <Progress value={uploadProgress} className="h-3 bg-white/30 rounded-full" />
                    <p className="text-slate-600 mt-2 text-center font-medium">{uploadProgress}% uploaded</p>
                  </div>
                )}
              </div>
            </Card>
            

            {/* Action Buttons */}
            <div className="flex justify-center">
              <Button
                onClick={handleGenerateTranscript}
                disabled={!uploadedFile || loadingStates.uploadingAudio}
                className="bg-gradient-to-r from-purple-500 to-blue-500 text-white py-6 px-12 rounded-2xl font-semibold text-lg shadow-lg shadow-purple-500/25 btn-blue-hover disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:hover:transform-none"
              >
                {loadingStates.uploadingAudio ? (
                  <>
                    <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <FileText className="w-6 h-6 mr-3" />
                    Generate Transcript
                  </>
                )}
              </Button>
            </div>

            {/* Error Display */}
            {errorStates.uploadError && (
              <div className="flex justify-center">
                <Card className="bg-red-50 border-red-200 rounded-2xl p-4 max-w-md">
                  <div className="flex items-center gap-3 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <p className="text-sm">{errorStates.uploadError}</p>
                  </div>
                </Card>
              </div>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Audio Language Selector */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-4 headline-enhanced">Audio Language</h3>
              <p className="text-slate-500 text-sm mb-4">Select the language of your audio file for better transcription accuracy</p>
              <Select value={selectedAudioLanguage} onValueChange={setSelectedAudioLanguage}>
                <SelectTrigger className="bg-white/40 backdrop-blur-xl border-white/30 text-slate-700 rounded-2xl h-12">
                  <SelectValue placeholder="Select audio language" />
                </SelectTrigger>
                <SelectContent className="bg-white/90 backdrop-blur-xl border-white/30 rounded-2xl">
                  <SelectItem value="auto">Select audio language</SelectItem>
                  <SelectItem value="vietnamese">🇻🇳 Vietnamese</SelectItem>
                  <SelectItem value="english">🇬🇧 English</SelectItem>
                  <SelectItem value="japanese">🇯🇵 Japanese</SelectItem>
                </SelectContent>
              </Select>
              <div className="mt-3 space-y-2">
                <p className="text-slate-400 text-xs">
                  💡 <strong>Vietnamese audio:</strong> Shows Vietnamese transcription only
                </p>
                <p className="text-slate-400 text-xs">
                  🌍 <strong>Other languages:</strong> Shows original language + Vietnamese translation
                </p>
              </div>
            </Card>

            {/* Tools Grid */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-6 headline-enhanced">Content Tools</h3>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { icon: Archive, label: "Archive", color: "bg-green-500" },
                  { icon: Palette, label: "Design", color: "bg-pink-500" },
                  { icon: Globe, label: "Web", color: "bg-cyan-500" },
                  { icon: Smartphone, label: "Mobile", color: "bg-purple-500" },
                  { icon: Film, label: "Video", color: "bg-red-500" },
                  { icon: Mic, label: "Audio", color: "bg-orange-500" },
                ].map((item, index) => (
                  <div key={index} className="text-center group cursor-pointer flex flex-col items-center">
                    <div className="w-16 h-16 bg-white/40 backdrop-blur-xl rounded-3xl flex items-center justify-center mb-3 border border-white/30 shadow-lg btn-blue-hover">
                      <div className={`w-8 h-8 ${item.color} rounded-2xl flex items-center justify-center`}>
                        <item.icon className="w-4 h-4 text-white" />
                      </div>
                    </div>
                    <span className="text-sm text-slate-600 font-medium text-center block">{item.label}</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Stats Card */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-4 headline-enhanced">Progress</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-2 rounded-xl btn-blue-hover cursor-pointer">
                  <span className="text-slate-600">Audio Files Processed</span>
                  <span className="font-bold text-slate-800">24</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-xl btn-blue-hover cursor-pointer">
                  <span className="text-slate-600">Ideas Generated</span>
                  <span className="font-bold text-slate-800">156</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-xl btn-blue-hover cursor-pointer">
                  <span className="text-slate-600">Content Created</span>
                  <span className="font-bold text-slate-800">89</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>

      {/* Transcript Modal */}
      <Dialog open={showTranscript} onOpenChange={setShowTranscript}>
        <DialogContent className="modal-fullscreen bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 z-50">
          <div className="modal-fullscreen-content p-6">
            <DialogHeader>
              <div className="flex-1">
                <DialogTitle className="headline-modal">Generated Transcript</DialogTitle>
                <p className="text-sm text-slate-600 mt-1">
                  Review and edit your transcript • {transcriptData.length} items • {transcriptData.filter(item => !item.removed).length} selected
                </p>
              </div>
            </DialogHeader>
            <div className="modal-fullscreen-body mt-6">
              {transcriptData.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="w-12 h-12 mx-auto text-slate-400 mb-4" />
                  <p className="text-slate-500 text-lg font-medium">No transcript data available</p>
                  <p className="text-slate-400 text-sm">Upload an audio file and generate transcript to see data here</p>
                </div>
              ) : (
                <div className="transcript-table-container h-full border border-slate-200 rounded-lg">
                  <table className="transcript-table w-full" role="table" aria-label="Transcript data table">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-center py-3 px-2 sm:px-4 text-slate-700 font-semibold w-16 sm:w-20" scope="col">Remove</th>
                    <th className="text-left py-3 px-2 sm:px-4 text-slate-700 font-semibold w-24 sm:w-32" scope="col">Timestamp</th>
                    <th className="text-left py-3 px-2 sm:px-4 text-slate-700 font-semibold" scope="col">Transcript</th>
                  </tr>
                </thead>
                <tbody>
                  {transcriptData.map((item) => (
                  <tr
                    key={item.id}
                    className={`transition-all duration-300 rounded-lg border-l-4 ${
                      item.removed
                        ? "bg-red-50/80 border-l-red-400 shadow-sm hover:bg-red-100/80 hover:shadow-md"
                        : "border-l-transparent btn-blue-hover"
                    }`}
                    role="row"
                    aria-label={item.removed ? `Transcript item marked for removal: ${item.text}` : `Transcript item: ${item.text}`}
                  >
                    <td className="py-3 px-2 sm:px-4">
                      <div className="flex items-center justify-center gap-2">
                        {item.removed && (
                          <div
                            className="flex items-center justify-center w-5 h-5 bg-red-100 rounded-full"
                            title="AI marked for removal"
                            role="img"
                            aria-label="Warning: This transcript segment has been marked for removal by AI quality assessment"
                          >
                            <AlertTriangle className="w-3 h-3 text-red-500" aria-hidden="true" />
                          </div>
                        )}
                        <Checkbox
                          checked={item.removed}
                          onCheckedChange={() => toggleTranscriptRemove(item.id)}
                          className={`transition-colors duration-200 ${
                            item.removed
                              ? "border-red-400 data-[state=checked]:bg-red-500 data-[state=checked]:border-red-500"
                              : "border-slate-300 hover:border-slate-400"
                          }`}
                        />
                        <Label htmlFor={`transcript-${item.id}`} className="sr-only">
                          Remove transcript item {item.id}
                        </Label>
                      </div>
                    </td>
                    <td className="py-3 px-2 sm:px-4">
                      <span className={`font-mono text-xs sm:text-sm font-medium transition-colors duration-300 ${
                        item.removed
                          ? "text-red-400 line-through"
                          : "text-slate-600"
                      }`}>
                        {item.timeline}
                      </span>
                    </td>
                    <td className="py-3 px-2 sm:px-4">
                      <div className="flex items-center gap-3">
                        <div className="flex-1">
                          {/* Show original language content first if it exists and is different from Vietnamese */}
                          {item.originalText && item.language !== 'vietnamese' && (
                            <div className="mb-2">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="language-label-original">
                                  {item.language === 'english' ? '🇬🇧 English' :
                                   item.language === 'japanese' ? '🇯🇵 Japanese' :
                                   `Original (${item.language})`}
                                </span>
                              </div>
                              <span
                                className={`block text-sm sm:text-base leading-relaxed transition-all duration-300 ${
                                  item.removed
                                    ? "line-through text-red-400 opacity-75"
                                    : "text-slate-600"
                                }`}
                              >
                                {item.originalText}
                              </span>
                            </div>
                          )}

                          {/* Vietnamese translation */}
                          <div>
                            {item.originalText && item.language !== 'vietnamese' && (
                              <div className="flex items-center gap-2 mb-1">
                                <span className="language-label-vietnamese">
                                  🇻🇳 Vietnamese Translation
                                </span>
                              </div>
                            )}
                            <span
                              className={`block text-sm sm:text-base leading-relaxed transition-all duration-300 ${
                                item.removed
                                  ? "line-through text-red-400 opacity-75"
                                  : "text-slate-700 font-medium"
                              }`}
                            >
                              {item.text}
                            </span>
                          </div>
                        </div>

                        {item.removed && (
                          <div className="flex items-center gap-1" role="status" aria-label="This transcript segment has been marked for removal by AI quality assessment">
                            <X className="w-3 h-3 text-red-500" aria-hidden="true" />
                            <span className="text-xs text-red-600 font-semibold bg-red-100 border border-red-200 px-2 py-1 rounded-md whitespace-nowrap shadow-sm">
                              AI Excluded
                            </span>
                            <span className="sr-only">This segment was automatically marked for removal due to low quality content such as filler words or interruptions</span>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                  </tbody>
                </table>
                </div>
              )}
            </div>
            <div className="flex gap-4 pt-4 mt-6">
              <Button className="flex-1 bg-green-500 text-white rounded-2xl py-3 btn-blue-hover">
                <Download className="w-5 h-5 mr-2" />
                Export Transcript
              </Button>
              <Button
                onClick={handleGenerateIdeas}
                disabled={loadingStates.generatingIdeas || transcriptData.length === 0}
                className="flex-1 bg-gradient-to-r from-orange-500 to-pink-500 text-white rounded-2xl py-3 btn-blue-hover disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
              >
                {loadingStates.generatingIdeas ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Lightbulb className="w-5 h-5 mr-2" />
                    Create Ideas
                  </>
                )}
              </Button>
            </div>

            {/* Error Display for Ideas */}
            {errorStates.ideasError && (
              <div className="mt-4">
                <Card className="bg-red-50 border-red-200 rounded-2xl p-4">
                  <div className="flex items-center gap-3 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <p className="text-sm">{errorStates.ideasError}</p>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Ideas Modal */}
      <Dialog open={showIdeas} onOpenChange={setShowIdeas}>
        <DialogContent className="modal-fullscreen bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 z-50">
          <div className="modal-fullscreen-content p-6">
            <DialogHeader>
              <div className="flex items-center gap-3">
                <Button
                  onClick={() => {
                    setShowTranscript(true)
                    setShowIdeas(false)
                  }}
                  className="w-10 h-10 bg-white/40 backdrop-blur-xl border-white/30 rounded-xl p-0 btn-blue-hover"
                >
                  <ArrowLeft className="w-5 h-5 text-slate-700" />
                </Button>
                <div className="flex-1">
                  <DialogTitle className="headline-modal">💡 Generated Ideas</DialogTitle>
                  <p className="text-sm text-slate-600 mt-1">
                    Select an idea to generate content • {ideaData.length} ideas available
                  </p>
                </div>
              </div>
            </DialogHeader>
            <div className="modal-fullscreen-body overflow-x-auto mt-6">
            <RadioGroup value={selectedIdeaId?.toString() || ""} onValueChange={handleIdeaSelection}>
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold w-12">Select</th>
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold">Paragraph</th>
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold">Timestamp</th>
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold">Main Idea</th>
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold">Sub Idea</th>
                    <th className="text-left py-3 px-4 text-slate-700 font-semibold">Format</th>
                  </tr>
                </thead>
                <tbody>
                  {ideaData.map((item) => (
                    <tr
                      key={item.id}
                      className={`btn-blue-hover transition-all duration-300 rounded-lg cursor-pointer ${
                        selectedIdeaId === item.id ? 'bg-blue-50/50 ring-2 ring-blue-200' : ''
                      }`}
                      onClick={() => handleIdeaSelection(item.id.toString())}
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center">
                          <RadioGroupItem value={item.id.toString()} id={`idea-${item.id}`} />
                          <Label htmlFor={`idea-${item.id}`} className="sr-only">
                            Select idea {item.id}
                          </Label>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="text-slate-700">
                          {/* Show original language content first if it exists and is different from Vietnamese */}
                          {item.originalParagraph && item.language !== 'vietnamese' && (
                            <div className="mb-2">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="language-label-original">
                                  {item.language === 'english' ? '🇬🇧 English' :
                                   item.language === 'japanese' ? '🇯🇵 Japanese' :
                                   `Original (${item.language})`}
                                </span>
                              </div>
                              <div className="text-sm text-slate-600 leading-relaxed">
                                {item.originalParagraph}
                              </div>
                            </div>
                          )}

                          {/* Vietnamese translation or Vietnamese-only content */}
                          <div>
                            {item.originalParagraph && item.language !== 'vietnamese' && (
                              <div className="flex items-center gap-2 mb-1">
                                <span className="language-label-vietnamese">
                                  🇻🇳 Vietnamese Translation
                                </span>
                              </div>
                            )}
                            <div className="text-sm text-slate-700 leading-relaxed font-medium">
                              {item.paragraph}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-slate-600 font-mono text-sm">{item.timestamp}</td>
                      <td className="py-3 px-4 text-slate-700 font-semibold">{item.mainIdea}</td>
                      <td className="py-3 px-4">
                        <div className="space-y-2">
                          {item.subIdeas.map((subIdea) => (
                            <div
                              key={subIdea.id}
                              className={`flex items-start gap-2 p-2 rounded-lg transition-all duration-300 cursor-pointer btn-blue-hover ${
                                subIdeaSelections[item.id]?.[subIdea.id] !== false
                                  ? 'bg-blue-50/50 border border-blue-200'
                                  : 'bg-slate-50/50 border border-slate-200'
                              }`}
                              onClick={(e) => {
                                e.stopPropagation()
                                toggleSubIdeaSelection(item.id, subIdea.id)
                              }}
                            >
                              <input
                                type="checkbox"
                                checked={subIdeaSelections[item.id]?.[subIdea.id] !== false}
                                onChange={() => toggleSubIdeaSelection(item.id, subIdea.id)}
                                className="mt-0.5 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                                onClick={(e) => e.stopPropagation()}
                              />
                              <span className="text-sm text-slate-600 leading-relaxed flex-1">
                                {subIdea.text}
                              </span>
                            </div>
                          ))}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <Select
                          value={item.format}
                          onValueChange={(value) => updateIdeaFormat(item.id, value)}
                        >
                          <SelectTrigger
                            className="bg-white/50 border-white/30 text-slate-700 rounded-xl"
                            onClick={(e: React.MouseEvent) => e.stopPropagation()}
                          >
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent className="bg-white/90 backdrop-blur-xl border-white/30 rounded-xl">
                            <SelectItem value="Video">📹 Video</SelectItem>
                            <SelectItem value="Blog">📝 Blog</SelectItem>
                            <SelectItem value="Post">📱 Post</SelectItem>
                            <SelectItem value="Infographic">📊 Infographic</SelectItem>
                          </SelectContent>
                        </Select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </RadioGroup>
            </div>
            <div className="space-y-4 pt-4 mt-6">
              {/* Selection Status */}
              {selectedIdea && (
                <div className="bg-blue-50/50 border border-blue-200 rounded-2xl p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                    <div>
                      <p className="text-sm font-medium text-blue-800">Selected Idea:</p>
                      <p className="text-blue-700">{selectedIdea.mainIdea}</p>
                      <p className="text-xs text-blue-600">Format: {selectedIdea.format}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-4">
                <Button
                  onClick={handleGenerateContent}
                  disabled={loadingStates.generatingContent || !selectedIdea}
                  className="w-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 text-white py-4 rounded-2xl font-bold text-lg shadow-lg shadow-purple-500/25 btn-blue-hover disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
                >
                  {loadingStates.generatingContent ? (
                    <>
                      <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                      Generating Content...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-6 h-6 mr-3" />
                      {selectedIdea ? 'Generate Content' : 'Select an Idea First'}
                    </>
                  )}
                </Button>
              </div>
            </div>

            {/* Error Display for Content Generation */}
            {errorStates.contentError && (
              <div className="mt-4">
                <Card className="bg-red-50 border-red-200 rounded-2xl p-4">
                  <div className="flex items-center gap-3 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <p className="text-sm">{errorStates.contentError}</p>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Content Modal */}
      <Dialog open={showContentModal} onOpenChange={setShowContentModal}>
        <DialogContent className="modal-fullscreen bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 z-50">
          <div className="modal-fullscreen-content p-6">
            <DialogHeader>
              <div className="flex items-center gap-3">
                <Button
                  onClick={handleBackToIdeas}
                  className="w-10 h-10 bg-white/40 backdrop-blur-xl border-white/30 rounded-xl p-0 btn-blue-hover"
                >
                  <ArrowLeft className="w-5 h-5 text-slate-700" />
                </Button>
                <div className="flex-1">
                  <DialogTitle className="headline-modal">
                    Generated Content
                  </DialogTitle>
                  {selectedIdea && (
                    <p className="text-sm text-slate-600 mt-1">
                      Based on: <span className="font-medium text-slate-700">{selectedIdea.mainIdea}</span>
                    </p>
                  )}
                </div>
              </div>
            </DialogHeader>
            <div className="modal-fullscreen-body space-y-6 mt-6">
            {/* Selected Idea Information */}
            {selectedIdea && (
              <Card className="bg-gradient-to-r from-blue-50/50 to-purple-50/50 border-blue-200/50 rounded-2xl p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-slate-800 mb-2 headline-enhanced">Selected Idea</h3>
                    <p className="text-slate-700 font-medium mb-1">{selectedIdea.mainIdea}</p>
                    <p className="text-slate-600 text-sm mb-3">{selectedIdea.subIdea}</p>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-slate-500">Content Format:</span>
                      <span className="px-3 py-1 bg-white/60 rounded-full text-sm font-medium text-slate-700">
                        {selectedIdea.format === 'Video' && '📹'}
                        {selectedIdea.format === 'Blog' && '📝'}
                        {selectedIdea.format === 'Post' && '📱'}
                        {selectedIdea.format === 'Infographic' && '📊'}
                        {selectedIdea.format}
                      </span>
                    </div>
                  </div>
                </div>
              </Card>
            )}

            {/* Generated Content Display */}
            {generatedContent ? (
              <Card className="bg-white/50 backdrop-blur-sm border-white/30 rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-slate-800 headline-enhanced">Generated Content</h3>
                  <div className="flex gap-2">
                    <Button
                      onClick={handleCopyContent}
                      className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-xl text-sm btn-blue-hover"
                    >
                      {copied ? (
                        <>
                          <Check className="w-4 h-4 mr-2" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4 mr-2" />
                          Copy
                        </>
                      )}
                    </Button>
                    <Button
                      onClick={handleNewContentGeneration}
                      className="bg-gradient-to-r from-slate-500 to-slate-600 text-white px-4 py-2 rounded-xl text-sm btn-blue-hover"
                    >
                      <ArrowLeft className="w-4 h-4 mr-2" />
                      New Idea
                    </Button>
                    <Button
                      onClick={handleGenerateContent}
                      disabled={loadingStates.generatingContent}
                      className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-xl text-sm btn-blue-hover disabled:hover:transform-none"
                    >
                      {loadingStates.generatingContent ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Regenerating...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-4 h-4 mr-2" />
                          Regenerate
                        </>
                      )}
                    </Button>
                  </div>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  <div className="markdown-content">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({children}) => <h1 className="text-2xl font-bold text-slate-800 mb-4 mt-6 first:mt-0">{children}</h1>,
                        h2: ({children}) => <h2 className="text-xl font-bold text-slate-800 mb-3 mt-5 first:mt-0">{children}</h2>,
                        h3: ({children}) => <h3 className="text-lg font-semibold text-slate-700 mb-2 mt-4 first:mt-0">{children}</h3>,
                        h4: ({children}) => <h4 className="text-base font-semibold text-slate-700 mb-2 mt-3 first:mt-0">{children}</h4>,
                        p: ({children}) => <p className="mb-3 text-slate-700 leading-relaxed">{children}</p>,
                        ul: ({children}) => <ul className="list-disc list-inside mb-4 space-y-1 text-slate-700 pl-4">{children}</ul>,
                        ol: ({children}) => <ol className="list-decimal list-inside mb-4 space-y-1 text-slate-700 pl-4">{children}</ol>,
                        li: ({children}) => <li className="text-slate-700 leading-relaxed mb-1">{children}</li>,
                        strong: ({children}) => <strong className="font-bold text-slate-800">{children}</strong>,
                        em: ({children}) => <em className="italic text-slate-700">{children}</em>,
                        code: ({children}) => <code className="bg-slate-100 text-slate-800 px-2 py-1 rounded text-sm font-mono">{children}</code>,
                        pre: ({children}) => <pre className="bg-slate-100 text-slate-800 p-4 rounded-lg overflow-x-auto mb-4 text-sm font-mono border">{children}</pre>,
                        blockquote: ({children}) => <blockquote className="border-l-4 border-blue-300 pl-4 py-2 italic text-slate-600 mb-4 bg-blue-50 rounded-r-lg">{children}</blockquote>,
                        hr: () => <hr className="border-slate-300 my-6" />,
                        table: ({children}) => <table className="w-full border-collapse border border-slate-300 mb-4 rounded-lg overflow-hidden">{children}</table>,
                        th: ({children}) => <th className="border border-slate-300 px-3 py-2 bg-slate-100 font-semibold text-left">{children}</th>,
                        td: ({children}) => <td className="border border-slate-300 px-3 py-2">{children}</td>,
                      }}
                    >
                      {generatedContent}
                    </ReactMarkdown>
                  </div>
                </div>
              </Card>
            ) : selectedIdea && !loadingStates.generatingContent ? (
              <Card className="bg-white/30 backdrop-blur-sm border-white/30 rounded-2xl p-8 text-center">
                <div className="text-slate-500">
                  <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium mb-2">Ready to Generate Content</p>
                  <p className="text-sm">
                    Click "Generate Content" in the Ideas modal to create content for "{selectedIdea.mainIdea}"
                  </p>
                </div>
              </Card>
            ) : loadingStates.generatingContent ? (
              <Card className="bg-white/30 backdrop-blur-sm border-white/30 rounded-2xl p-8 text-center">
                <div className="text-slate-600">
                  <Loader2 className="w-12 h-12 mx-auto mb-4 animate-spin" />
                  <p className="text-lg font-medium mb-2">Generating Content...</p>
                  <p className="text-sm">Please wait while we create your content</p>
                </div>
              </Card>
            ) : null}

              {/* Error Display for Content Generation */}
              {errorStates.contentError && (
                <Card className="bg-red-50 border-red-200 rounded-2xl p-4">
                  <div className="flex items-center gap-3 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <div>
                      <p className="font-medium">Content Generation Failed</p>
                      <p className="text-sm">{errorStates.contentError}</p>
                    </div>
                  </div>
                </Card>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
