import React, { useState } from 'react';
import { Upload, FileText, Play, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const PodcastGenerator = () => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [podcast, setPodcast] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Replace with your actual API endpoint
      const response = await fetch('/api/generate-podcast', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate podcast');
      }

      const data = await response.json();
      setPodcast(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">PDF to Podcast Generator</h1>
          <p className="text-gray-600">Convert any PDF into an engaging podcast</p>
        </div>

        {/* Main Card */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Generate New Podcast</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  PDF URL
                </label>
                <div className="relative">
                  <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 
                             focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter PDF URL..."
                    required
                  />
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 
                             bg-blue-500 text-white px-4 py-1 rounded-md
                             hover:bg-blue-600 transition-colors disabled:opacity-50"
                  >
                    {isLoading ? (
                      <div className="flex items-center">
                        <Loader2 className="animate-spin" size={18} />
                        <span className="ml-2">Processing...</span>
                      </div>
                    ) : (
                      <div className="flex items-center">
                        <Upload size={18} />
                        <span className="ml-2">Generate</span>
                      </div>
                    )}
                  </button>
                </div>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
            {error}
          </div>
        )}

        {/* Generated Podcast */}
        {podcast && (
          <Card>
            <CardHeader>
              <CardTitle>Generated Podcast</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <FileText className="text-gray-500" />
                  <div>
                    <h3 className="font-medium">{podcast.title}</h3>
                    <p className="text-sm text-gray-500">{podcast.duration}</p>
                  </div>
                </div>
                <audio
                  controls
                  className="w-full"
                  src={podcast.audioUrl}
                >
                  Your browser does not support the audio element.
                </audio>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default PodcastGenerator;