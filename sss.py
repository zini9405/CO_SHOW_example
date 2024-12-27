    def step_selection(self, H_local, H_global):
        """
        Select important steps using step-level Multi-Head Attention.

        Args:
        - H_local: Local embeddings for each step (batch_size, num_steps, hidden_dim).
        - H_global: Global embedding for the entire sequence (batch_size, hidden_dim).

        Returns:
        - H_selected: Combined embedding of important steps and global information (batch_size, hidden_dim * 2).
        - step_scores: Attention scores for each step (batch_size, num_steps).
        """
        # Perform step-level attention
        H_step, step_scores = self.step_attention(H_local, H_local, H_local, need_weights=True)
        
        # Reduce step_scores to match H_local dimensions
        step_scores = step_scores.mean(dim=1)  # Shape: (batch_size, num_steps)

        # Reshape step_scores for broadcasting
        step_scores = step_scores.unsqueeze(-1)  # Shape: (batch_size, num_steps, 1)

        # Weighted sum of H_local using step_scores
        weighted_local = torch.sum(step_scores * H_local, dim=1)  # Shape: (batch_size, hidden_dim)

        # Combine global embedding and weighted local embedding
        H_selected = torch.cat([H_global, weighted_local], dim=-1)  # Shape: (batch_size, hidden_dim * 2)

        return H_selected, step_scores.squeeze(-1)  # Squeeze for final attention scores