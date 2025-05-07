import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  VStack,
  HStack,
  Input,
  useToast,
} from '@chakra-ui/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { chatApi, Message } from '../services/api';

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatApi.sendMessage([...messages, userMessage]);
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to send message',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" h="100vh" py={4}>
      <Flex direction="column" h="full">
        <VStack flex={1} overflowY="auto" spacing={4} align="stretch">
          {messages.map((message, index) => (
            <Box
              key={index}
              bg={message.role === 'user' ? 'blue.100' : 'gray.100'}
              p={4}
              borderRadius="md"
              alignSelf={message.role === 'user' ? 'flex-end' : 'flex-start'}
              maxW="80%"
              whiteSpace="pre-wrap"
              wordBreak="break-word"
              overflowX="auto"
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </Box>
          ))}
          <div ref={messagesEndRef} />
        </VStack>

        <HStack mt={4}>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button
            colorScheme="blue"
            onClick={handleSend}
            isLoading={isLoading}
            loadingText="Sending..."
          >
            Send
          </Button>
        </HStack>
      </Flex>
    </Container>
  );
}

export default Chat; 