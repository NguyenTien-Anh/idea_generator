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
  Loader2,
  Copy,
  Check,
} from "lucide-react"

export default function Component() {
  const [selectedRole, setSelectedRole] = useState<"editor" | "creator">("editor")
  const [selectedLanguage, setSelectedLanguage] = useState("en")
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

  // API hook for backend integration
  const {
    loadingStates,
    errorStates,
    uploadVideo,
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
    if (!file.type.startsWith('video/') && !file.type.startsWith('audio/')) {
      toast.error('Please upload a video or audio file')
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
      toast.error('Please upload a video file first')
      return
    }

    clearError('uploadError')

    try {
      const result = await uploadVideo(uploadedFile)
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
      // Create a more detailed idea text for better content generation
      const ideaText = `${selectedIdea.mainIdea}. ${selectedIdea.subIdea || ''}`

      const result = await generateContentFromIdea(selectedIdea.format.toLowerCase(), ideaText.trim())
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
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 font-['Inter']">
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
                  <h1 className="text-2xl font-bold text-slate-800">Video Ideas Generator</h1>
                  <p className="text-slate-600">Discover a treasure of ideas from video</p>
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
                <Button className="w-12 h-12 bg-white/30 backdrop-blur-xl border-white/20 rounded-2xl p-0 hover:bg-white/40">
                  <Bell className="w-5 h-5 text-slate-700" />
                </Button>
                <Button className="w-12 h-12 bg-white/30 backdrop-blur-xl border-white/20 rounded-2xl p-0 hover:bg-white/40">
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
                  <h2 className="text-3xl font-bold mb-2">Video Ideas</h2>
                  <p className="text-white/70">AI-powered content generation from your videos</p>
                </div>
              </div>
              <div className="text-white/50 text-sm">Ready to transform your content</div>
            </Card>

            {/* Role Selector */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">Who are you?</h3>
              <div className="flex gap-4">
                {["editor", "creator"].map((role) => (
                  <Button
                    key={role}
                    onClick={() => setSelectedRole(role as "editor" | "creator")}
                    className={`flex-1 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 ${
                      selectedRole === role
                        ? "bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg shadow-purple-500/25"
                        : "bg-white/40 backdrop-blur-xl text-slate-700 border border-white/30 hover:bg-white/50"
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
                  accept="video/*"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="border-2 border-dashed border-slate-300 rounded-3xl p-12 transition-all duration-300 group-hover:border-purple-400 group-hover:bg-white/10 bg-white/5 backdrop-blur-xl">
                  <div className="flex flex-col items-center space-y-4">
                    <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-blue-500 rounded-3xl flex items-center justify-center shadow-lg">
                      <Cloud className="w-10 h-10 text-white" />
                    </div>
                    <div className="text-center">
                      <h3 className="text-2xl font-semibold text-slate-700 mb-2">Upload Video File</h3>
                      <p className="text-slate-500">Drag and drop your video here or click to browse</p>
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
                disabled={!uploadedFile || loadingStates.uploadingVideo}
                className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white py-6 px-12 rounded-2xl font-semibold text-lg shadow-lg shadow-purple-500/25 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                {loadingStates.uploadingVideo ? (
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
            {/* Language Selector */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">Select Language</h3>
              <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                <SelectTrigger className="bg-white/40 backdrop-blur-xl border-white/30 text-slate-700 rounded-2xl h-12">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white/90 backdrop-blur-xl border-white/30 rounded-2xl">
                  <SelectItem value="vi">🇻🇳 Vietnamese</SelectItem>
                  <SelectItem value="en">🇬🇧 English</SelectItem>
                  <SelectItem value="jp">🇯🇵 Japanese</SelectItem>
                </SelectContent>
              </Select>
            </Card>

            {/* Tools Grid */}
            <Card className="bg-white/20 backdrop-blur-2xl border-white/30 rounded-3xl p-6 shadow-xl">
              <h3 className="text-xl font-semibold text-slate-800 mb-6">Content Tools</h3>
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
                    <div className="w-16 h-16 bg-white/40 backdrop-blur-xl rounded-3xl flex items-center justify-center mb-3 border border-white/30 shadow-lg hover:scale-105 transition-all duration-200 group-hover:bg-white/50">
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
              <h3 className="text-xl font-semibold text-slate-800 mb-4">Progress</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Videos Processed</span>
                  <span className="font-bold text-slate-800">24</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Ideas Generated</span>
                  <span className="font-bold text-slate-800">156</span>
                </div>
                <div className="flex justify-between items-center">
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
        <DialogContent className="max-w-4xl bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 rounded-3xl z-50">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">Generated Transcript</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {transcriptData.map((item) => (
              <div
                key={item.id}
                className={`p-4 rounded-2xl transition-all duration-300 ${
                  item.removed ? "bg-red-100" : "bg-white/50 backdrop-blur-sm"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="text-sm text-slate-500 font-mono mb-2">{item.timeline}</div>
                    <div
                      className={`text-slate-700 transition-all duration-300 ${
                        item.removed ? "line-through text-slate-400" : ""
                      }`}
                    >
                      {item.text}
                    </div>
                  </div>
                  <Checkbox
                    checked={item.removed}
                    onCheckedChange={() => toggleTranscriptRemove(item.id)}
                    className="ml-4"
                  />
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-4 pt-4">
            <Button className="flex-1 bg-green-500 hover:bg-green-600 text-white rounded-2xl py-3">
              <Download className="w-5 h-5 mr-2" />
              Export Transcript
            </Button>
            <Button
              onClick={handleGenerateIdeas}
              disabled={loadingStates.generatingIdeas || transcriptData.length === 0}
              className="flex-1 bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white rounded-2xl py-3 disabled:opacity-50 disabled:cursor-not-allowed"
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
        </DialogContent>
      </Dialog>

      {/* Ideas Modal */}
      <Dialog open={showIdeas} onOpenChange={setShowIdeas}>
        <DialogContent className="max-w-6xl bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 rounded-3xl z-50">
          <DialogHeader>
            <div className="flex items-center gap-3">
              <Button
                onClick={() => {
                  setShowTranscript(true)
                  setShowIdeas(false)
                }}
                className="w-10 h-10 bg-white/40 backdrop-blur-xl border-white/30 rounded-xl p-0 hover:bg-white/50 transition-all duration-200"
              >
                <ArrowLeft className="w-5 h-5 text-slate-700" />
              </Button>
              <div className="flex-1">
                <DialogTitle className="text-2xl font-bold">💡 Generated Ideas</DialogTitle>
                <p className="text-sm text-slate-600 mt-1">
                  Select an idea to generate content • {ideaData.length} ideas available
                </p>
              </div>
            </div>
          </DialogHeader>
          <div className="overflow-x-auto">
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
                      className={`hover:bg-white/30 transition-all duration-300 rounded-lg cursor-pointer ${
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
                      <td className="py-3 px-4 text-slate-700">{item.paragraph}</td>
                      <td className="py-3 px-4 text-slate-600 font-mono text-sm">{item.timestamp}</td>
                      <td className="py-3 px-4 text-slate-700 font-semibold">{item.mainIdea}</td>
                      <td className="py-3 px-4 text-slate-600">{item.subIdea}</td>
                      <td className="py-3 px-4">
                        <Select
                          value={item.format}
                          onValueChange={(value) => updateIdeaFormat(item.id, value)}
                          onClick={(e) => e.stopPropagation()}
                        >
                          <SelectTrigger className="bg-white/50 border-white/30 text-slate-700 rounded-xl">
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
          <div className="space-y-4 pt-4">
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
                className="w-full bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 hover:from-cyan-600 hover:via-purple-600 hover:to-pink-600 text-white py-4 rounded-2xl font-bold text-lg shadow-lg shadow-purple-500/25 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
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
        </DialogContent>
      </Dialog>

      {/* Content Modal */}
      <Dialog open={showContentModal} onOpenChange={setShowContentModal}>
        <DialogContent className="max-w-4xl max-h-[80vh] bg-white/90 backdrop-blur-xl border-white/30 text-slate-800 rounded-3xl z-50">
          <DialogHeader>
            <div className="flex items-center gap-3">
              <Button
                onClick={handleBackToIdeas}
                className="w-10 h-10 bg-white/40 backdrop-blur-xl border-white/30 rounded-xl p-0 hover:bg-white/50 transition-all duration-200"
              >
                <ArrowLeft className="w-5 h-5 text-slate-700" />
              </Button>
              <div className="flex-1">
                <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
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
          <div className="space-y-6">
            {/* Selected Idea Information */}
            {selectedIdea && (
              <Card className="bg-gradient-to-r from-blue-50/50 to-purple-50/50 border-blue-200/50 rounded-2xl p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-slate-800 mb-2">Selected Idea</h3>
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
                  <h3 className="text-xl font-bold text-slate-800">Generated Content</h3>
                  <div className="flex gap-2">
                    <Button
                      onClick={handleCopyContent}
                      className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-2 rounded-xl text-sm"
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
                      className="bg-gradient-to-r from-slate-500 to-slate-600 hover:from-slate-600 hover:to-slate-700 text-white px-4 py-2 rounded-xl text-sm"
                    >
                      <ArrowLeft className="w-4 h-4 mr-2" />
                      New Idea
                    </Button>
                    <Button
                      onClick={handleGenerateContent}
                      disabled={loadingStates.generatingContent}
                      className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white px-4 py-2 rounded-xl text-sm"
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
                  <div className="text-slate-700 whitespace-pre-line leading-relaxed">
                    {generatedContent}
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
        </DialogContent>
      </Dialog>
    </div>
  )
}
