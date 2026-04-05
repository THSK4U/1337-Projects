/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:00:02 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/03 16:34:10 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	unsigned char	*v_dst;
	unsigned char	*v_src;
	size_t			i;

	if (!dest && !src)
		return (NULL);
	i = 0;
	v_dst = (unsigned char *)dest;
	v_src = (unsigned char *)src;
	while (i < n)
	{
		v_dst[i] = v_src[i];
		i++;
	}
	return (dest);
}
