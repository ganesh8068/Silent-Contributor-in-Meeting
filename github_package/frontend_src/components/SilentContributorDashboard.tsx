import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Mic, MessageSquare, FileText, CheckSquare, AlertTriangle } from 'lucide-react';

interface Participant {
  participant: {
    id: number;
    meeting_id: number;
    user_id: number;
    speaking_time: number;
    engagement_score: number;
  };
  user: {
    id: number;
    username: string;
    email: string;
  };
  chat_messages: number;
  document_activities: number;
  task_activities: number;
}

const ParticipantCard = ({ participant }: { participant: Participant }) => {
  // This would come from the API in a real implementation
  const mockData = {
    name: participant.user.username,
    speakingTime: participant.participant.speaking_time,
    chatMessages: participant.chat_messages || 5,
    documentActivities: participant.document_activities || 2,
    taskActivities: participant.task_activities || 3,
    engagementScore: participant.participant.engagement_score || 45,
  };

  const getScoreColor = (score: number): string => {
    if (score < 30) return "text-red-500";
    if (score < 60) return "text-yellow-500";
    return "text-green-500";
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{mockData.name}</CardTitle>
          <Badge variant={mockData.speakingTime < 60 ? "destructive" : "default"}>
            {mockData.speakingTime < 60 ? "Silent Contributor" : "Active Speaker"}
          </Badge>
        </div>
        <CardDescription>Engagement Score</CardDescription>
        <div className="flex items-center gap-2">
          <Progress value={mockData.engagementScore} className="h-2" />
          <span className={`font-bold ${getScoreColor(mockData.engagementScore)}`}>
            {mockData.engagementScore.toFixed(1)}%
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <Mic className="h-4 w-4 text-muted-foreground" />
            <span>Speaking: {Math.floor(mockData.speakingTime / 60)}m {mockData.speakingTime % 60}s</span>
          </div>
          <div className="flex items-center gap-2">
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
            <span>Chat: {mockData.chatMessages} messages</span>
          </div>
          <div className="flex items-center gap-2">
            <FileText className="h-4 w-4 text-muted-foreground" />
            <span>Docs: {mockData.documentActivities} edits</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckSquare className="h-4 w-4 text-muted-foreground" />
            <span>Tasks: {mockData.taskActivities} items</span>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        {mockData.speakingTime < 60 && mockData.engagementScore > 30 && (
          <div className="flex items-center gap-2 text-amber-500 text-sm">
            <AlertTriangle className="h-4 w-4" />
            <span>Silent but engaged through other channels</span>
          </div>
        )}
      </CardFooter>
    </Card>
  );
};

const SilentContributorDashboard = () => {
  const [silentContributors, setSilentContributors] = useState<Participant[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, this would fetch data from the API
    // For now, we'll use mock data
    const mockSilentContributors = [
      {
        participant: {
          id: 1,
          meeting_id: 1,
          user_id: 1,
          speaking_time: 30,
          engagement_score: 65
        },
        user: {
          id: 1,
          username: "Alex Johnson",
          email: "alex@example.com"
        },
        chat_messages: 8,
        document_activities: 4,
        task_activities: 5
      },
      {
        participant: {
          id: 2,
          meeting_id: 1,
          user_id: 2,
          speaking_time: 15,
          engagement_score: 42
        },
        user: {
          id: 2,
          username: "Sam Taylor",
          email: "sam@example.com"
        },
        chat_messages: 5,
        document_activities: 2,
        task_activities: 3
      },
      {
        participant: {
          id: 3,
          meeting_id: 1,
          user_id: 3,
          speaking_time: 45,
          engagement_score: 28
        },
        user: {
          id: 3,
          username: "Jordan Lee",
          email: "jordan@example.com"
        },
        chat_messages: 2,
        document_activities: 1,
        task_activities: 0
      }
    ];

    setTimeout(() => {
      setSilentContributors(mockSilentContributors);
      setLoading(false);
    }, 1000);
  }, []);

  const chartData = silentContributors.map(contributor => ({
    name: contributor.user.username,
    speaking: contributor.participant.speaking_time,
    chat: contributor.chat_messages * 10, // Scaled for visualization
    documents: contributor.document_activities * 15, // Scaled for visualization
    tasks: contributor.task_activities * 20, // Scaled for visualization
  }));

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Silent Contributor Detector</h1>
      
      <Tabs defaultValue="dashboard">
        <TabsList className="mb-4">
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>
        
        <TabsContent value="dashboard">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              <p>Loading participants data...</p>
            ) : (
              silentContributors.map(contributor => (
                <ParticipantCard 
                  key={contributor.participant.id} 
                  participant={contributor} 
                />
              ))
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="analytics">
          <Card>
            <CardHeader>
              <CardTitle>Contribution Comparison</CardTitle>
              <CardDescription>
                Comparing verbal vs. non-verbal contributions across participants
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={chartData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="speaking" name="Speaking Time (s)" fill="#8884d8" />
                    <Bar dataKey="chat" name="Chat Activity" fill="#82ca9d" />
                    <Bar dataKey="documents" name="Document Activity" fill="#ffc658" />
                    <Bar dataKey="tasks" name="Task Activity" fill="#ff8042" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default SilentContributorDashboard;
