namespace DevKnowledgeBase.API.DTOs;

public class CreateArticleDto
{
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public Guid? CategoryId { get; set; }
    public string? CreatedBy { get; set; }
    public List<Guid> TagIds { get; set; } = new();
}
