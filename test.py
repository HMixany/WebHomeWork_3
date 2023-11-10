groups_files = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR']
}


result = 'JPEG' in [groups_files[key] for key in groups_files.keys()]
print(result)
print(groups_files.values())
print([groups_files[key] for key in groups_files.keys()])