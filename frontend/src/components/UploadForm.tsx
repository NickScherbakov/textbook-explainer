/**
 * @license
 * Copyright (c) 2023 Nick Scherbakov
 * 
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  LinearProgress,
  Alert,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';
import axios from 'axios';

// Стилизованный компонент для загрузки файлов
const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

function UploadForm() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [audienceType, setAudienceType] = useState('student');
  const [complexityLevel, setComplexityLevel] = useState('2');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleAudienceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAudienceType(event.target.value);
  };

  const handleComplexityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setComplexityLevel(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setError('Пожалуйста, выберите файл для загрузки');
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_audience', audienceType);
    formData.append('complexity_level', complexityLevel);

    try {
      // В реальном приложении здесь будет запрос к вашему API
      // const response = await axios.post('/api/upload', formData);
      // Для демонстрации просто имитируем успешный ответ
      setTimeout(() => {
        const mockDocumentId = 'doc_' + Math.random().toString(36).substr(2, 9);
        setUploading(false);
        navigate(`/documents/${mockDocumentId}`);
      }, 2000);
    } catch (err) {
      setUploading(false);
      setError('Произошла ошибка при загрузке файла. Пожалуйста, попробуйте снова.');
      console.error('Upload error:', err);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Загрузка документа
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <form onSubmit={handleSubmit}>
        <Box sx={{ mb: 3 }}>
          <Button
            component="label"
            variant="contained"
            startIcon={<CloudUploadIcon />}
            sx={{ mb: 2 }}
            disabled={uploading}
          >
            Выбрать файл
            <VisuallyHiddenInput type="file" onChange={handleFileChange} accept=".pdf,.png,.jpg,.jpeg" />
          </Button>
          
          {file && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              Выбран файл: {file.name}
            </Typography>
          )}
        </Box>

        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">Целевая аудитория</FormLabel>
          <RadioGroup value={audienceType} onChange={handleAudienceChange} row>
            <FormControlLabel value="student" control={<Radio />} label="Ученик" />
            <FormControlLabel value="teacher" control={<Radio />} label="Преподаватель" />
            <FormControlLabel value="researcher" control={<Radio />} label="Исследователь" />
          </RadioGroup>
        </FormControl>

        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">Уровень сложности (1-простой, 5-сложный)</FormLabel>
          <RadioGroup value={complexityLevel} onChange={handleComplexityChange} row>
            <FormControlLabel value="1" control={<Radio />} label="1" />
            <FormControlLabel value="2" control={<Radio />} label="2" />
            <FormControlLabel value="3" control={<Radio />} label="3" />
            <FormControlLabel value="4" control={<Radio />} label="4" />
            <FormControlLabel value="5" control={<Radio />} label="5" />
          </RadioGroup>
        </FormControl>

        {uploading && <LinearProgress sx={{ mb: 2 }} />}

        <Button 
          type="submit" 
          variant="contained" 
          color="primary" 
          disabled={uploading || !file}
          fullWidth
        >
          Загрузить и обработать
        </Button>
      </form>
    </Paper>
  );
}

export default UploadForm;
