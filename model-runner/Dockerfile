FROM ollama/ollama

EXPOSE 11434

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Override the default ollama entrypoint
ENTRYPOINT ["/start.sh"]