namespace DevKnowledgeBase.API.DTOs;

public class UpdateArticleDto
{
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public Guid? CategoryId { get; set; }
    public List<Guid> TagIds { get; set; } = new();
}
